### Running the application
```sh
docker-compose up
```
Now hit **localhost:8005** and you can see the application running.

You can find elasticsearch on **localhost:9200**


### Closing the application

```sh
docker-compose down
```


### preprocessing summary:

title and text are combined and used as info for further calculations
1. translate to english
2. tokenize
3. use Porterstemmer for stemming
4. remove duplicates, i.e. frequency of any word in a document will be 1 because more frequency doesn't really add any value in this particular application
5. get color information from the above processed text
6. get condition information from above processed text
7. use the posting date see how old the item is


Then add the relevant keys to the crawled json files. 
Index the json files.
get queries. 
  for each query calculate the relevance scores using tf-idf similarity, condition, color and posting date
  then group the queries according according to average relevance score and the distance between them
