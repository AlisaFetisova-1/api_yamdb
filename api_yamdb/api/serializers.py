from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from reviews.models import Comment, Review, Title, Category, Genre


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        fields = ("id", "text", "author", "score", "pub_date")
        model = Review

    def validate(self, obj):
        title_id = self.context['view'].kwargs.get('title_id')
        request = self.context['request']
        title = get_object_or_404(Title, id=title_id)
        if request.method == 'POST':
            if Review.objects.filter(
                author=request.user, title=title
            ).exists():
                raise serializers.ValidationError(
                    'Вы уже оставли свой ответ'
                )
        return obj


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        fields = ("id", "text", "author", "pub_date")
        model = Comment


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
