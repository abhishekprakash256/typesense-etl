"""
search the data in the typesense 
"""

import typesense
import mongo_helper_kit
from bson.objectid import ObjectId
from config import DB_NAME, COLLECTION_NAME, MONGO_HOST_NAME, FILE_PATH


#make the client 
client = typesense.Client({
  'api_key': 'test_key',
  'nodes': [{
    'host': 'localhost',
    'port': '8108',
    'protocol': 'http'
  }],
  'connection_timeout_seconds': 2
})




#make the search paramaters
search_parameters = {
  'q'         : 'neual netwo',
  'query_by'  : 'article_data'

}


#get the res
res = client.collections['articles'].documents.search(search_parameters)

#print the res 
#print(res)


#get the id number from the data
id_numbers = [hit['document']['id'] for hit in res.get('hits', [])]
print(id_numbers)


#get the schema
#export_output = client.collections['articles'].documents.export()
#print(export_output)


#get the data from mongo using the id number 
mongo_client = mongo_helper_kit.create_mongo_client(MONGO_HOST_NAME)


db = mongo_client[DB_NAME]
collection = db[COLLECTION_NAME]

obj_id = ObjectId(id_numbers[0])


# Find the document
doc = collection.find_one({"_id": obj_id})

# Print the result

#if doc:
#    print(doc)
#else:
#    print("No document found with that _id.")


# Execute the query and return results (sorted by `created_at` field)



results = []

for id in id_numbers :

  obj_id = ObjectId(id)

  # Find the document
  doc = collection.find_one({"_id": obj_id})

  # Extract the necessary fields based on the new design
  card = {
      "card_title": doc.get("article_name", ""),
      "card_para": doc.get("article_para", ""),
      "img_src": doc.get("article_image", ""),
      "card_url": doc.get("article_link", "")
  }
  results.append(card)

print(results)


#mongo sesrach data 
mongo_helper = mongo_helper_kit.Helper_fun(MONGO_HOST_NAME)

print(mongo_helper.search_database(DB_NAME, COLLECTION_NAME, "neural"))

