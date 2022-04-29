from store.models import Collection
from django.contrib.auth.models import User
from rest_framework import status
import pytest
from model_bakery import baker


@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return api_client.post('/store/collections/', collection)
    return do_create_collection


@pytest.mark.django_db
class TestCreateCollection():
    def test_if_user_is_anonymous_returns_401(self, create_collection):
        # ACT
        response = create_collection({'title': 'a'})
        # assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, create_collection, authenticate):
        # ACT
        authenticate()
        response = create_collection({'title': 'a'})
        # assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_return_400(self, create_collection, authenticate):
        # ACT
        authenticate(is_staff=True)
        response = create_collection({'title': ''})
        # assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    def test_if_data_is_valid_return_201(self, create_collection, authenticate):
        # ACT
        authenticate(is_staff=True)
        response = create_collection({'title': 'a'})
        # assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestRetriveCollection:
    def test_if_collection_exists_return_200(self, api_client):
        # Arrange
        collection = baker.make(Collection)
        # Act
        response = api_client.get(f'/store/collections/{collection.id}/')
        print(response)
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': collection.id,
            'title': collection.title,
            'products_count':0
        }
