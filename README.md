# typesense-etl


## Setup the repo 

### To setup the docker container

```bash

- docker run -d --name mongo --network my_network -p 27017:27017 mongo:latest
- ingest the data using mongo helper kit , python3 prototype-v2/data_ingestion.py
- export TYPESENSE_API_KEY=test_key                     #the api key will change in prod
- docker run -d --name typesense --network my_network -p 8108:8108 -v$(pwd)/typesense-data:/data typesense/typesense:29.0.rc30 --data-dir /data --api-key=$TYPESENSE_API_KEY --enable-cors 


```


### Reqs 


```bash 

pip install typesense 

git install git+ssh://git@github.com/abhishekprakash256/mongo-helper-kit.git


```