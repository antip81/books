import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase
from store.serializers import BooksSerializer

from store.models import Book


class BookApiTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username="test_username")
        self.book_1 = Book.objects.create(name="test book 1", price="25", author_name="Author 1", owner=self.user)
        self.book_2 = Book.objects.create(name="test book 2", price="55", author_name="Author 2")
        self.book_3 = Book.objects.create(name="test book 3 Author 1", price="55", author_name="Author 3")

    def test_get(self):
        url = reverse("book-list")
        response = self.client.get(url)
        serializer_data = BooksSerializer([self.book_1, self.book_2, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_filter(self):
        url = reverse("book-list")
        response = self.client.get(url, data={"price": 55})
        serializer_data = BooksSerializer([self.book_2, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_search(self):
        url = reverse("book-list")
        response = self.client.get(url, data={"search": "Author 1"})
        serializer_data = BooksSerializer([self.book_1, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_ordering(self):
        url = reverse("book-list")
        response = self.client.get(url, data={"ordering": "-author_name"})
        serializer_data = BooksSerializer([self.book_3, self.book_2, self.book_1], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(3, Book.objects.all().count())
        url = reverse("book-list")
        data = {
            "name": "Programming in Python 3",
            "price": 150,
            "author_name": "Mark Summerfield"
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data, content_type="application/json")

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Book.objects.all().count())
        self.assertEqual(self.user, Book.objects.last().owner)

    def test_update(self):
        url = reverse("book-detail", args=(self.book_1.id,))
        data = {
            "name": self.book_1.name,
            "price": 575,
            "author_name": self.book_1.author_name
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data, content_type="application/json")

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # self.book_1 = Book.objects.get(id=self.book_1.id)
        self.book_1.refresh_from_db()
        self.assertEqual(575, self.book_1.price)

    def test_update_not_owner(self):
        url = reverse("book-detail", args=(self.book_1.id,))
        data = {
            "name": self.book_1.name,
            "price": 575,
            "author_name": self.book_1.author_name
        }
        json_data = json.dumps(data)

        self.user2 = User.objects.create(username="test_username2")
        self.client.force_login(self.user2)
        response = self.client.put(url, data=json_data, content_type="application/json")

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual({'detail': ErrorDetail(string='You do not have permission to perform this action.',
                                                code='permission_denied')}, response.data)

        self.book_1.refresh_from_db()
        self.assertEqual(25, self.book_1.price)

    def test_update_not_owner_but_staff(self):
        url = reverse("book-detail", args=(self.book_1.id,))
        data = {
            "name": self.book_1.name,
            "price": 575,
            "author_name": self.book_1.author_name
        }
        json_data = json.dumps(data)

        self.user2 = User.objects.create(username="test_username2", is_staff=True)
        self.client.force_login(self.user2)
        response = self.client.put(url, data=json_data, content_type="application/json")

        self.book_1.refresh_from_db()
        self.assertEqual(575, self.book_1.price)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_delete(self):
        self.assertEqual(3, Book.objects.all().count())

        url = reverse("book-detail", args=(self.book_1.id,))
        self.client.force_login(self.user)
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, Book.objects.all().count())

    def test_delete_not_owner(self):
        self.assertEqual(3, Book.objects.all().count())

        url = reverse("book-detail", args=(self.book_1.id,))

        self.user2 = User.objects.create(username="test_username2")
        self.client.force_login(self.user2)
        response = self.client.delete(url)

        self.assertEqual({'detail': ErrorDetail(string='You do not have permission to perform this action.',
                                                code='permission_denied')}, response.data)

        self.assertEqual(3, Book.objects.all().count())

    def test_delete_not_owner_but_staff(self):
        self.assertEqual(3, Book.objects.all().count())

        url = reverse("book-detail", args=(self.book_1.id,))

        self.user2 = User.objects.create(username="test_username2", is_staff=True)
        self.client.force_login(self.user2)
        response = self.client.delete(url)

        self.assertEqual(2, Book.objects.all().count())

    def test_get_id(self):
        url = reverse("book-detail", args=(self.book_1.id,))
        response = self.client.get(url)
        serializer_data = BooksSerializer(self.book_1).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
