# Django-ElasticSearch-DRF

This project demonstrates the integration of Elasticsearch with Django and Django-Rest-Framework (DRF) to build a simple search API. Elasticsearch is a powerful search engine widely used by companies. This project is a basic implementation of Elasticsearch aims to simplify the process of integrating Elasticsearch with Django and provide a comprehensive guide for building search functionality.

## Project Overview
The project consists of a Django app with two models:
- Category: Represents a category with a title.
- Article: Represents an article with a title and a category (related to the Category model).

## Features
- Allow users to search articles by title using Elasticsearch.
- Enable users to filter articles by category using Elasticsearch.
- Create an auto-complete API for articles.

## Running the Project Locally
Before diving into Django, make sure you have an Elasticsearch instance running locally. The preferred method is using Docker and Docker-Compose. The project includes a Dockerfile for Django and a docker-compose.yml file with two services: web and elasticsearch.

### Load the dummy data
The project consists of a `demo-data.json` with some dummy data to populate the database. Run the following command to load the dummy data in the database.

```
python manage.py load_data
```

### To run the containers:
```
docker-compose up -d
```

Visit `localhost:8000` to ensure everything is working.

## APIs in Action
`DocumentViewSet` automatically creates different APIs:

- List and retrieve records.
- Normal functionality (search, filter, etc.).
- Auto-complete functionality.
- Functional suggestions.

### Examples:

- List: ```127.0.0.1:8000/article-search```
    - ```127.0.0.1:8000/article-search```

- Search: ```127.0.0.1:8000/article-search?search=sports```
    - ```127.0.0.1:8000/article-search?search=<term>```
    - If you want to search on multiple terms, you can do it using:
        ```localhost:8000/article-search?search=<term1>&search=<term2>```

- Filter: ```127.0.0.1:8000/article-search?category=2```
    - ```127.0.0.1:8000/article-search?category=<id>```
    - If you want to filter by multiple categories:
        ```127.0.0.1:8000/article-search?category=id1__id2__id3```

- Auto-Suggest: ```127.0.0.1:8000/article-search/suggest?title__completion=how```
    - ```127.0.0.1:8000/article-search/suggest?title__completion=<some_text>```

## Other Files

### documents.py
In the `documents.py` file, we define the structure of the Elasticsearch document (`ArticleDocument`) that corresponds to our Django model (`Article`). This file outlines how the data from Django should be stored in Elasticsearch.

- Document Definition:
    - We create a class named `ArticleDocument` that extends `Document`. This class represents the schema of the document that will be stored in Elasticsearch.

- Field Mapping:
    - For each field in our Django model that we want to index in Elasticsearch, such as `title` and `category`, we specify how it should be stored in the Elasticsearch document.
    - For the `title` field:
        - It is defined as a text field in Elasticsearch.
        - Sub-fields include `'raw'` for regular search and `'suggest'` for auto-complete.
    - For the `category` field:
        - As it is a relation to another model, it is defined as an object field in Elasticsearch.
        - Sub-fields within the object include `'id'` (an integer) and `'title'` (a text field with a raw keyword field for search).

- Index Configuration:
    - We specify that the Elasticsearch index for storing this document is named 'articles'. This naming convention helps organize data within Elasticsearch.

- Django Model Association:
    - We associate our Elasticsearch document (`ArticleDocument`) with our Django model (`Article`). This linkage ensures that changes in the Django model are automatically reflected in the corresponding Elasticsearch document.

### signals.py
In the `signals.py` file, we implement Django signals to automate the synchronization of data between our Django models and Elasticsearch indexes. This ensures that changes to the models trigger updates in the corresponding Elasticsearch documents.

- Post-Save and Post-Delete Signals:
    - We utilize two key signals:
        - **post_save Signal:**
            - Triggered after a model instance is saved.
            - We use this signal to update the Elasticsearch index when a new record is added or an existing record is modified.
        - **post_delete Signal:**
            - Triggered after a model instance is deleted.
            - This signal is employed to update the Elasticsearch index when a record is removed.

- Signal Implementation:
    - The `update_document` and `delete_document` functions are connected to the respective signals. They perform the following actions:
        - **update_document:**
            - Retrieves the app label, model name, and instance from the signal.
            - Checks if the signal pertains to the `articles` app and the `article` model.
            -If true, iterates through related instances and updates the corresponding Elasticsearch documents.

        - **delete_document:**
            - Similar to `update_document` but handles the deletion event.
            - Removes the Elasticsearch documents corresponding to the deleted model instances.

- Automation of Index Updates:
    - By employing these signals, we automate the process of updating Elasticsearch indexes whenever changes occur in the associated Django models. This ensures consistency between the Django application's data and the Elasticsearch search index.
    - In essence, `signals.py` enhances the integration between Django and Elasticsearch, providing a mechanism for real-time updates and synchronization of data between the two environments.