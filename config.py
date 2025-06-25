# config.py

import os 

# MongoDB configurations
DB_NAME = "test-main-database"
COLLECTION_NAME = "test-article-collections"
MONGO_HOST_NAME = "localhost"
API_KEY = "test_key"


# File path
#FILE_PATH = "test_data.json"

#get the curr dir 
curr_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(curr_dir) 


#data file path 
FILE_PATH = parent_dir + "/test_data.json"


ARTICLE_SCHEMA = {
    "name": "articles",
    "enable_nested_fields": True,
    "fields": [
        {"name": "id", "type": "string"},  # Required primary key
        {"name": "article_name", "type": "string"},
        {"name": "slug", "type": "string"},
        {"name": "article_image", "type": "string"},
        {"name": "article_para", "type": "string"},
        {"name": "section_name", "type": "string", "facet": True},
        {"name": "id_number", "type": "int32"},

        # Flattened nested fields
        {"name": "article_data.title", "type": "string[]"},
        {"name": "article_data.article_para", "type": "string[]"},
        {"name": "article_data.markdown_data", "type": "string[]"},

        # Links
        {"name": "github_url", "type": "string"},
        {"name": "linkedin_url", "type": "string"},
        {"name": "twitter_url", "type": "string"},
        {"name": "leetcode_url", "type": "string"},
        {"name": "gitlab_url", "type": "string"},
        {"name": "kaggle_url", "type": "string"},
        {"name": "medium_url", "type": "string"},
        {"name": "demo_link", "type": "string"},
        {"name": "article_link", "type": "string"},
        {"name": "more_link", "type": "string"}
    ],
    "default_sorting_field": "id_number"
}
