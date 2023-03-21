from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import CharField, EmailField, ValidationError
from rest_framework.validators import UniqueValidator
from reviews.models import Category, Comment, Genre, Review, Title, User


class UserSerializer(serializers.ModelSerializer):
    username = CharField(validators=[UniqueValidator(
        queryset=User.objects.all())],
        required=True,
    )
    email = EmailField(validators=[UniqueValidator(
        queryset=User.objects.all())],
        required=True,
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')

    def validate_username(self, username):
        if username == 'me':
            raise ValidationError(
                'Вы не можете использовать "me"!')
        return username


class MeSerializer(serializers.ModelSerializer):
    username = CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')
        read_only_fields = ('role',)

    def validate_username(self, username):
        if username == 'me':
            raise ValidationError(
                'Вы не можете использовать "me"!')
        return username


class GetTokenSerializer(serializers.ModelSerializer):
    username = CharField(required=True)
    confirmation_code = CharField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id',)

    def validate_data(self, data):
        if len(data['slug']) > 50:
            raise serializers.ValidationError()
        return data


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id',)

    def validate_data(self, data):
        if not data.is_valid():
            raise serializers.ValidationError()
        return data


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category')
        model = Title


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
                    'Вы уже оставили свой ответ'
                )
        return obj


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        fields = ("id", "text", "author", "pub_date")
        model = Comment
