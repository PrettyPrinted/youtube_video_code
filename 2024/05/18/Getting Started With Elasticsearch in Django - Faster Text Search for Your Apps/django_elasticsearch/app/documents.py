from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry

from .models import Book 

@registry.register_document
class BookDocument(Document):
    class Index:
        name = "books"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Book
        fields = ["title", "author", "description"]