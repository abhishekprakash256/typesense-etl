# typesense-etl


## Setup the repo 

### To setup the 

```bash

- docker run -d --name mongo-db -p 27017:27017 mongo
- ingest the data using mongo helper kit , python3 prototype-v2/data_ingestion.py
- export TYPESENSE_API_KEY=test_key                     #the api key will change in prod
- docker run -d --name typesense -p 8108:8108 -v$(pwd)/typesense-data:/data typesense/typesense:29.0.rc30 --data-dir /data --api-key=$TYPESENSE_API_KEY --enable-cors 


```
