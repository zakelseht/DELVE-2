import datetime
from haystack import indexes
from . import models


class NoteIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')

    def get_model(self):
        return models.Combo

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(pk=1)

# class BookIndex(indexes.SearchIndex, indexes.Indexable):
#     text = indexes.CharField(document=True, use_template=True, template_name="search/book_text.txt")
#     title = indexes.CharField(model_attr='title')
#     authors = indexes.CharField()
#     def get_model(self):
#         return Book
#     def prepare_authors(self, obj):
#         return [ author.name for a in obj.authors.all()]
#     def index_queryset(self, using=None):
#         return self.get_model().objects.all()
