from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from articles.models import Article


@registry.register_document
class ArticleDocument(Document):
    title = fields.TextField(
        attr='title',
        fields={
            'raw': fields.TextField(),
            'suggest': fields.CompletionField(),
        }
    )
    category = fields.ObjectField(
        attr='category',
        properties={
            'id': fields.IntegerField(),
            'title': fields.TextField(
                attr='title',
                fields={
                    'raw': fields.KeywordField(),
                }
            )
        }
    )

    class Index:
        name = 'articles'

    class Django:
        model = Article

# This may seem complicated but we simply registered a document called ArticleDocument that is linked to 
#        the model Article. We then specified the fields that we want to index in ElasticSearch.
# The first field is the title, which is a TextField with two properties.
# raw – This is the normal ElasticSearch text field that we will use for search functionality.
# suggest – This is a completion field that is used for auto-complete functionality.
# The next field is the category which is a relation field, but ElasticSearch has no concept of relations.
# That's why we use the object field to save the whole category object, in Elasticsearch.
# We specify that the category field is an object, then in the properties, we specify the fields of category which are id and title.
        
# Keyword vs Text – Full vs. Partial Matches
# The primary difference between the text datatype and the keyword datatype is that text fields are analyzed at the time of indexing, 
# and keyword fields are not. What that means is, text fields are broken down into their individual terms at indexing to allow for partial matching, 
# while keyword fields are indexed as is.
# For example, a text field containing the value “Roosters crow everyday” 
# would get all of its individual components indexed: “Roosters”, “crow”, and “everyday”; 
# a query on any of those terms would return this string. 
# However, if the same string was stored as a keyword type, it would not get broken down. Only a search for the exact string “Roosters crow everyday” 
# would return it as a result. Because text fields are analyzed in this way, one consequence is that they’re not able to be sorted alphabetically. 
# A keyword field, on the other hand, can be sorted alphabetically in the typical fashion.