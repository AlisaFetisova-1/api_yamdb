from rest_framework import serializers
from rest_framework.serializers import CharField, EmailField, ValidationError
from rest_framework.validators import UniqueValidator
from reviews.models import User


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
    username = CharField(
        required=True)
    confirmation_code = CharField(
        required=True)

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
