import pytest
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.urls import reverse
from exhibition.models import Kitten, Breed, Rating
from tests.conftest import client, model_factory, token, authorized_client


@pytest.mark.django_db
def test_authorization(client):
    response = client.post(reverse('api:users-list'), data={'username': 'test', 'password': 'test'})
    assert response.status_code == 201
    assert User.objects.filter(username='test').exists() is True
    response = client.post(reverse('token_obtain_pair'), data={'username': 'test', 'password': 'test'})
    assert response.status_code == 200
    assert response.json().get('access') is not None
    refresh_token = response.json().get('refresh')
    assert refresh_token is not None
    response = client.post(reverse('token_refresh'), data={'refresh': refresh_token})
    assert response.status_code == 200


@pytest.mark.django_db
def test_list_breeds(client, model_factory):
    breeds = model_factory(Breed, _quantity=5)
    breeds_dicts = [model_to_dict(breed) for breed in breeds]
    response = client.get(reverse('api:breeds-list'))
    assert response.status_code == 200
    assert breeds_dicts.sort(key=lambda x: x['id']) == response.json().sort(key=lambda x: x['id'])


@pytest.mark.django_db
def test_list_kittens(client, model_factory):
    kittens = model_factory(Kitten, _quantity=5)
    kittens_dicts = [model_to_dict(kitten) for kitten in kittens]
    response = client.get(reverse('api:kittens-list'))
    assert response.status_code == 200
    assert kittens_dicts.sort(key=lambda x: x['id']) == response.json().sort(key=lambda x: x['id'])


@pytest.mark.django_db
def test_list_kittens_by_breed_filter(client, model_factory):
    kittens = model_factory(Kitten, _quantity=5)
    breed = model_to_dict(kittens[0].breed)
    breed_id = breed['id']
    response = client.get(f'{reverse("api:kittens-list")}?breed={breed_id}')
    assert response.status_code == 200
    kittens_dicts = [model_to_dict(kitten) for kitten in Kitten.objects.filter(breed=breed_id).all()]
    assert kittens_dicts == response.json()


@pytest.mark.django_db
def test_retrieve_kittens(client, model_factory):
    ratings = model_factory(Rating, _quantity=5)
    rating_obj = ratings[0]
    kitten = model_to_dict(rating_obj.kitten)
    kitten['rating'] = rating_obj.value
    response = client.get(reverse('api:kittens-detail', kwargs={'pk': kitten['id']}))
    assert response.status_code == 200
    assert kitten == response.json()


def test_create_kitten_authorization(client):
    response = client.post(reverse('api:kittens-list'),
                           data={})
    assert response.status_code == 401


@pytest.mark.django_db
def test_create_kitten(authorized_client, model_factory):
    breed = model_factory(Breed)
    response = authorized_client.post(reverse('api:kittens-list'),
                                      data={'color': 'black', 'age': 10, 'description': 'fat cat', 'breed': breed.id})
    assert response.status_code == 201
    kitten_objects = Kitten.objects.all()
    assert len(kitten_objects) == 1
    response_json = response.json()
    assert model_to_dict(kitten_objects[0]) == response_json


def test_update_kitten_authorization(client):
    response = client.put(reverse('api:kittens-detail', kwargs={'pk': 1}),
                          data={})
    assert response.status_code == 401


@pytest.mark.django_db
def test_update_kitten_permission(authorized_client, model_factory):
    kitten = model_factory(Kitten)
    response = authorized_client.put(reverse('api:kittens-detail', kwargs={'pk': kitten.id}),
                                     data={'color': 'color', 'age': 1, 'description': 'description',
                                           'breed': kitten.breed.id})
    assert response.status_code == 403


@pytest.mark.django_db
def test_update_kitten(authorized_client, model_factory):
    breed = model_factory(Breed)
    breed_id = breed.id
    authorized_client.post(reverse('api:kittens-list'),
                           data={'color': 'black', 'age': 10, 'description': 'fat cat', 'breed': breed_id})
    response = authorized_client.put(reverse('api:kittens-detail', kwargs={'pk': Kitten.objects.all()[0].id}),
                                     data={'color': 'color', 'age': 1, 'description': 'description',
                                           'breed': breed_id})
    assert response.status_code == 200
    assert model_to_dict(Kitten.objects.all()[0]) == response.json()


def test_partial_update_kitten_authorization(client):
    response = client.patch(reverse('api:kittens-detail', kwargs={'pk': 1}),
                            data={})
    assert response.status_code == 401


@pytest.mark.django_db
def test_partial_update_kitten_permission(authorized_client, model_factory):
    kitten = model_factory(Kitten)
    response = authorized_client.patch(reverse('api:kittens-detail', kwargs={'pk': kitten.id}),
                                       data={'color': 'color'})
    assert response.status_code == 403


@pytest.mark.django_db
def test_partial_update_kitten(authorized_client, model_factory):
    breed = model_factory(Breed)
    breed_id = breed.id
    authorized_client.post(reverse('api:kittens-list'),
                           data={'color': 'black', 'age': 10, 'description': 'fat cat', 'breed': breed_id})
    response = authorized_client.patch(reverse('api:kittens-detail', kwargs={'pk': Kitten.objects.all()[0].id}),
                                       data={'color': 'color'})
    assert response.status_code == 200
    assert model_to_dict(Kitten.objects.all()[0]) == response.json()


def test_delete_kitten_authorization(client):
    response = client.delete(reverse('api:kittens-detail', kwargs={'pk': 1}),
                             data={})
    assert response.status_code == 401


@pytest.mark.django_db
def test_delete_kitten_permission(authorized_client, model_factory):
    kitten = model_factory(Kitten)
    response = authorized_client.delete(reverse('api:kittens-detail', kwargs={'pk': kitten.id}))
    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_kitten(authorized_client, model_factory):
    breed = model_factory(Breed)
    breed_id = breed.id
    authorized_client.post(reverse('api:kittens-list'),
                           data={'color': 'black', 'age': 10, 'description': 'fat cat', 'breed': breed_id})
    kitten_id = Kitten.objects.all()[0].id
    response = authorized_client.delete(reverse('api:kittens-detail', kwargs={'pk': kitten_id}))
    assert response.status_code == 204
    assert Kitten.objects.filter(id=kitten_id).exists() is False


def test_create_rating_authorization(client):
    response = client.post(reverse('api:ratings-list'),
                           data={})
    assert response.status_code == 401


@pytest.mark.django_db
def test_create_rating_validation_own_kitten(authorized_client, model_factory):
    breed = model_factory(Breed)
    breed_id = breed.id
    authorized_client.post(reverse('api:kittens-list'),
                           data={'color': 'black', 'age': 10, 'description': 'fat cat', 'breed': breed_id})
    response = authorized_client.post(reverse('api:ratings-list'),
                                      data={'kitten': Kitten.objects.all()[0].id, 'value': 1})
    assert response.status_code == 400
    assert response.json()[0] == 'You can not evaluate your own kitten'


@pytest.mark.django_db
def test_create_rating_validation_same_kitten(authorized_client, model_factory):
    kitten = model_factory(Kitten)
    url = reverse('api:ratings-list')
    authorized_client.post(url, data={'kitten': kitten.id, 'value': 1})
    response = authorized_client.post(url, data={'kitten': kitten.id, 'value': 1})
    assert response.status_code == 400
    assert response.json()[0] == 'You can not evaluate same kitten more then once'


@pytest.mark.django_db
def test_create_rating(authorized_client, model_factory, token):
    kitten = model_factory(Kitten)
    response = authorized_client.post(reverse('api:ratings-list'), data={'kitten': kitten.id, 'value': 1})
    assert response.status_code == 201
    assert Kitten.objects.all()[0].get_rating() == 1
