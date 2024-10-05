from django.contrib.auth.models import User
from rest_framework import serializers

from exhibition.models import Breed, Kitten, Rating


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data: dict) -> User:
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user


class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = '__all__'


class KittenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kitten
        fields = '__all__'
        read_only_fields = ['id', 'creator']
        extra_kwargs = {
            'age': {'help_text': 'Age in full months'},
        }


class KittenRatingSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Kitten
        fields = ['id', 'color', 'age', 'description', 'breed', 'creator', 'rating']
        read_only_fields = ['id', 'creator']
        extra_kwargs = {
            'age': {'help_text': 'Age in full months'},
        }

    def get_rating(self, obj):
        return obj.get_rating()


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['kitten', 'value']
        extra_kwargs = {
            'value': {'help_text': 'Value from 1 to 5'},
        }
