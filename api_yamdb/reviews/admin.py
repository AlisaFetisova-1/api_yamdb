from django.contrib import admin
from .models import (Comment, Review,
                     Title, GenreTitle,
                     Genre, Category) 

admin.site.register(Comment)
admin.site.register(Review)
admin.site.register(GenreTitle)
admin.site.register(Title)
admin.site.register(Category)
admin.site.register(Genre)
