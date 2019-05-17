"""
Created on Mon May 13 04:15:27 2019

@author: mukund
"""

#import packages

from mtranslate import translate 
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import re
from collections import Counter
from .preprocessing import * 

class ad:
    
    """
    each ad consists of the following information and following methods
    
    """
    def __init__(self, price, size, title, descriptiion, location, indate ):
        self.price = price
        self.size = size
        self.title = title
        self.desc = descriptiion
        self.place = location
        self.indate = indate
        self.condition = 0
        self.text = self.title + " " + self.desc
        self.num_days()
        self.preprocess_text()
        self.get_color()
        self.get_condition()

    def translate_english(self):
        #translate text to english
        return translate(self.text,"en","auto")


    def tokenize(self): 
        
        #remove punctuation
        text = re.sub(r'[^\w\s]','',self.text)
            
        return word_tokenize(self.text.lower())


    def stemming(self, tokens):

        #using PorterStemmer to stem the words

        stemmer = PorterStemmer()
        result = []
        for i in tokens:
            result.append(stemmer.stem(i))

        return result


    def unique_words(self, tokens):
        #remove repeated words in the title and description
        dictionary = Counter(tokens)
        return list(dictionary.keys())


    def preprocess_text(self):
        self.text = self.translate_english()
        tokens = self.tokenize()
        stemmed_words = self.stemming(tokens)
        #return joined list of unique words in text
        unique_words = self.unique_words(stemmed_words)
        self.tokens =  unique_words  ##" ".join(unique_words)
        return


    def get_color(self):

        #extract color information from text
        common_colors = ["red","orange","yellow","green","blue","purple","brown"
        ,"magenta","tan","cyan","olive","maroon","navy","aquamarine","turquoise",
        "silver","lime","teal","indigo","violet","pink","black","white","gray","grey"]
        
        self.colors = [i for i in common_colors if i in self.tokens]
        return 

    def get_condition(self):

        #common product conditions. bare use - barely used and unus - unused
        #alternativs: use machine learning to train a simple classifier

        conditions = ['new', 'old', 'bare', 'unus', 'use', 'almost', 'very', 'good']
        condition = [i for i in conditions if i in self.tokens]
        if len(condition) == 1 and 'use'in condition :
             self.condition = 0.2
        elif ('good' in condition) or 'almost' in condition:
            self.condition = 0.4
        elif ('bare' in condition) or ('almost' in condition) or ('very' in condition):
            self.condition = 0.6
        elif ('unus' in condition):
            self.condition = 0.8
        elif len(condition) == 1 and 'new'in condition :
            self.condition = 1
        elif len(condition) == 0 or len(condition) > 3:
            self.condition = 0
        
        return

    

    def num_days(self):
        #number of days the product is unsold
        today = datetime.today().strftime('%m/%d/%Y')
        a = datetime.strptime(today, "%m/%d/%Y")
        b = datetime.strptime(self.indate, "%m/%d/%Y")
        delta = b - a
        self.days = delta.days
        return
