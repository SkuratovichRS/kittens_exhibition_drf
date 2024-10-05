from typing import Type

from django.contrib.auth.models import User
from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from exhibition.models import Kitten, Breed, Rating
from exhibition.permissions import authentication
from exhibition.serializers import KittenSerializer, UserSerializer, BreedSerializer, RatingSerializer, \
    KittenRatingSerializer


class KittenViewSet(ModelViewSet):
    queryset = Kitten.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['breed']

    def get_permissions(self) -> list:
        return authentication(self.action)

    def perform_create(self, serializer: KittenSerializer) -> None:
        serializer.save(creator=self.request.user)

    def perform_update(self, serializer: KittenSerializer) -> None:
        if serializer.instance.creator != self.request.user:
            raise PermissionDenied()
        serializer.save()

    def perform_destroy(self, instance: Kitten) -> None:
        if instance.creator != self.request.user:
            raise PermissionDenied()
        instance.delete()

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == 'retrieve':
            return KittenRatingSerializer
        return KittenSerializer


class UserViewSet(CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class BreedViewSet(ListModelMixin, GenericViewSet):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer


class RatingViewSet(CreateModelMixin, GenericViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def get_permissions(self) -> list:
        return authentication(self.action)

    def perform_create(self, serializer: RatingSerializer) -> None:
        user = self.request.user
        if Kitten.objects.filter(creator=user, id=self.request.data.get("kitten")).exists():
            raise ValidationError('You can not evaluate your own kitten')
        try:
            serializer.save(user=user)
        except IntegrityError:
            raise ValidationError('You can not evaluate same kitten more then once')
