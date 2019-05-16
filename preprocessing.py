#preprocessing functions


"""
import packages 
"""
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import re
from collections import Counter
from geopy.geocoders import Nominatim
import geopy.distance
from datetime import datetime
import itertools
from sklearn.feature_extraction.text import TfidfVectorizer

def get_coordinates(address):

	#get latitute and longitute from location name
	geolocator = Nominatim()
	location = geolocator.geocode(address)
	return (location.latitute, location.longitute)

	

def distance(location1, location2):
	#distance between two places on earth. only considering straight line distance
	return float(geopy.distance.vincenty(location1,location2).km)



def least_distance(locations):

	if len(locations) == 1:
		return 0
	elif len(locations) == 2:
		return distance(locations[0], locations[1])
	elif len(locations) == 3:
		d = []
		d[0] = distance(locations[0], locations[1])
		d[1] = distance(locations[2], locations[1])
		d[2] = distance(locations[2], locations[0])
		d.sort()
		return d[0]+d[1]
	elif len(locations) == 4:
		l = list(itertools.permutations(locations))
		d = []
		for i in range(len(l)):
			d[i] = distance(l[i][0], l[i][1]) + distance(l[i][2], l[i][1]) + distance(l[i][2], l[i][3])
		d.sort()
		return d[0]

	else:
		return 0



def tfidf_vectors(descriptions):
	vectorizer = TfidfVectorizer(min_df=0, )
	X = vectorizer.fit_transform(descriptions)
    return




def find_color(query):
    #extract color information from text

    text = re.sub(r'[^\w\s]','',query)
    tokens = word_tokenize(text.lower())
    stemmer = PorterStemmer()
    result = []
    for i in tokens:
    	result.append(stemmer.stem(i))
    tokens = result

    common_colors = ["red","orange","yellow","green","blue","purple","brown"
    ,"magenta","tan","cyan","olive","maroon","navy","aquamarine","turquoise",
    "silver","lime","teal","indigo","violet","pink","black","white","gray","grey"]
    dictionary = Counter(tokens)
    tokens = list(dictionary.keys())
    color = [i for i in common_colors if i in tokens]
    return tokens, color










