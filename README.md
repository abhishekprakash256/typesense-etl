# typesense-etl

A simple ETL pipeline to ingest data from MongoDB into Typesense and enable search functionality. This setup uses Docker for containerized MongoDB and Typesense instances.

---

## 📦 Setup

### 1. Start Docker Containers

Create a shared Docker network:

```bash
docker network create my_network
```

Run MongoDB:

```bash
docker run -d \
  --name mongo \
  --network my_network \
  -p 27017:27017 \
  mongo:latest
```

Set your Typesense API key (you can change this in production):

```bash
export TYPESENSE_API_KEY=test_key
```

Run Typesense:

```bash
docker run -d \
  --name typesense \
  --network my_network \
  -p 8108:8108 \
  -v $(pwd)/typesense-data:/data \
  typesense/typesense:29.0.rc30 \
  --data-dir /data \
  --api-key=$TYPESENSE_API_KEY \
  --enable-cors
```

---

### 2. Install Requirements

Clone this repo and install dependencies:

```bash
pip install typesense
pip install git+ssh://git@github.com/abhishekprakash256/mongo-helper-kit.git
```

> Make sure you have SSH access set up for GitHub to clone the private helper repo.

---

### 3. Ingest Data

Use the provided helper script to ingest data from MongoDB and index it into Typesense:

```bash
python3 etl_typesense.py
```

This script:

* Fetches data from the configured MongoDB collection
* Flattens and transforms documents to match the Typesense schema
* Inserts the documents into your Typesense collection

---

## 🔍 Search Functionality

Once data is indexed, you can query the Typesense server:

```python
import typesense

client = typesense.Client({
    'api_key': 'test_key',  # or your production key
    'nodes': [{
        'host': 'localhost',
        'port': '8108',
        'protocol': 'http'
    }],
    'connection_timeout_seconds': 2
})

search_parameters = {
    'q': 'your search query',
    'query_by': 'field1,field2'
}

results = client.collections['your_collection_name'].documents.search(search_parameters)
print(results)
```

### Run the test file manually 

```bash
 python3 -m test.test_search    # from the parent folder

```


---

## 🧪 Notes

* This is a dev prototype. In production, use secrets management for API keys.
* The Typesense container uses persistent volume via `typesense-data` folder.
