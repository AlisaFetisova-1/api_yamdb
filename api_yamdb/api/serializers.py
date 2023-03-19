from rest_framework import serializers
from reviews.models import Category, Genre, Title


class CategorySerial(serializers.ModelSerializer):

    class Meta:
        fields = ('name',)
        model = Category


class GenreSerial(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genre


class TitleSerial(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Title
