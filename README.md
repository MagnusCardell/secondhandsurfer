
# Second Hand Surfer

A search engine for finding the perfect bundle of items scraped from Blocket.se. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

To run this project you need to have docker and docker-compose installed. With docker installed, all other dependencies and installs will be managed by the docker-image and kept isolated inside the container. 


### Start

In the project root, you can now build and start the individual services: 

```
docker-compose build
docker-compose up 
```

Which will start the elasticsearch, flask api, and frontend services. Now hit **localhost:8005** and you can see the application running. To setup a debug environment, we recommend starting the servies individually 

```
docker-compose up elasticsearch
docker-compose up frontend
py app.py
```
Then visit **localhost:8005** for the web interface, and **localhost:9200** for elasticsearch. 

### Closing the application

```sh
docker-compose down
```


## Technology stack

* [Docker-compose](https://docs.docker.com/compose//) - Containerization
* [Python flask](http://flask.pocoo.org/) - Web API and algorithms
* [Vue.js](https://vuejs.org/) - Frontend framework

## Authors

* **Mukund Seethamraju** 
* **Robert Siwerz** 
* **Magnus Cardell** 

