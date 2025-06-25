"""
The file for the ingestion of the data from mongo to typesense container
"""



import json
import os
import sys
import requests
import typesense
import mongo_helper_kit
from bson import ObjectId
from config import DB_NAME, COLLECTION_NAME, MONGO_HOST_NAME, FILE_PATH , API_KEY, ARTICLE_SCHEMA
from typesense.exceptions import TypesenseClientError



#make the client 
client = typesense.Client({
  'api_key': API_KEY,
  'nodes': [{
    'host': 'localhost',
    'port': '8108',
    'protocol': 'http'
  }],
  'connection_timeout_seconds': 2
})



#delete the collection if created 
#client.collections['articles'].delete()



def check_client():
    """
    The function to check the client health
    """
    try:
        collections = client.collections.retrieve()
        print("Connected successfully!")
        return True

    except Exception as e:
        print("Connection failed!")
        print("Error:", e)
        return False


def check_container_health():
    """
    The function to check the container health
    """
    url = "http://localhost:8108/health"

    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            return True
        else:
            print(f"Typesense health check failed with status: {response.status_code}")
            return False
        
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Typesense: {e}")
        return False



#check the container health
print(check_container_health())

#check the client container
print(check_client())



#make the schema
#this is the nested schema 
#other stragety can be using the flatten the data and then use it 


#create the collection
#if not check_container_health and not check_client(): 

client.collections.create(ARTICLE_SCHEMA)

#get the schema
retrieve_response = client.collections['articles'].retrieve()
print(retrieve_response)


# Convert _id to id as string, keep the rest unchanged
def convert_id(doc):
    doc['id'] = str(doc['_id'])  # Rename and convert ObjectId
    del doc['_id']               # Remove original _id
    return doc


#make the mongo cleint
mongo_client = mongo_helper_kit.create_mongo_client(MONGO_HOST_NAME)

#the db name
db = mongo_client[DB_NAME]
collection = db[COLLECTION_NAME]


# Example: Fetching documents from MongoDB
mongo_documents = list(collection.find({}))

#get all mongo data
#print(mongo_documents)


# Convert _id to string for Typesense
cleaned_docs = [convert_id(doc) for doc in mongo_documents]

#insert the data into the typesnse 

response = client.collections['articles'].documents.import_(
    cleaned_docs,
    {'action': 'upsert'}  # 'upsert' means insert or update
)


#export the data and check
export_output = client.collections['articles'].documents.export()
print(export_output)