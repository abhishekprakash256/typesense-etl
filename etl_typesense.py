"""
The file for the ingestion of the data from mongo to typesense container
"""
import logging
import requests
import typesense
import mongo_helper_kit
from bson import ObjectId
from config import DB_NAME, COLLECTION_NAME, MONGO_HOST_NAME, FILE_PATH , API_KEY, ARTICLE_SCHEMA
from typesense.exceptions import TypesenseClientError
from typesense.exceptions import ObjectNotFound





# Configure logging
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("ingestion.log"),       # <- logs to file
        logging.StreamHandler()                     # <- logs to console
    ]
)
logger = logging.getLogger(__name__)



#make the typesense client 
typesense_client = typesense.Client({
  'api_key': API_KEY,
  'nodes': [{
    'host': 'localhost',
    'port': '8108',
    'protocol': 'http'
  }],
  'connection_timeout_seconds': 2
})

#make the mongo cleint
mongo_client = mongo_helper_kit.create_mongo_client(MONGO_HOST_NAME)



#try to check for the client
try:
    typesense_client.collections['articles'].delete()
    logger.info("Collection 'articles' deleted.")
except ObjectNotFound:
    logger.info("Collection 'articles' does not exist. Skipping deletion.")
except Exception as e:
    logger.info(f"Unexpected error occurred while deleting collection: {e}")




def check_client():
    """
    The function to check the client health
    """
    try:
        collections = typesense_client.collections.retrieve()
        logger.info("Connected successfully!")
        return True

    except Exception as e:
        logger.info("Connection failed!")
        logger.info("Error:", e)
        return False



def check_container_health(url="http://localhost:8108/health") -> bool:
    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            return True
        logger.warning(f"Health check failed: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Connection to Typesense failed: {e}")
    return False
    

# Convert _id to id as string, keep the rest unchanged
def convert_id(doc):
    doc['id'] = str(doc['_id'])  # Rename and convert ObjectId
    del doc['_id']               # Remove original _id
    return doc





def ingest_data():
    """
    The main function to run the logic for ingestion
    """

    #check the container and the client 

    container_health = check_container_health()

    if not container_health:

        logger.error("Typesense container is not healthy.")

        return 
    
    client_health = check_client()

    if not client_health :

        logger.error("The client is not initilaized properly")

        return 
    
    #create the article schema
    typesense_client.collections.create(ARTICLE_SCHEMA)

    #get the schema
    #retrieve_response = typesense_client.collections['articles'].retrieve()
    #print(retrieve_response)


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
    response = typesense_client.collections['articles'].documents.import_(
        cleaned_docs,
        {'action': 'upsert'}  # 'upsert' means insert or update
    )

    for r in response:
        if not r.get('success'):
            logger.warning(f"Failed to index document ID {r.get('id')}: {r.get('error')}")

    logger.info("Ingestion completed.")


    #export the data and check
    export_output = typesense_client.collections['articles'].documents.export()
    logger.info(export_output)

    return True



if __name__ == "__main__":

    ingest_data()





