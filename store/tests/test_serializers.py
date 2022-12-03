from unittest import TestCase
from store.serializers import BooksSerializer

from store.models import Book


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        book_1 = Book.objects.create(name="test book 1", price="25", author_name="test author 1")
        book_2 = Book.objects.create(name="test book 2", price="55", author_name="test author 2")
        data = BooksSerializer([book_1, book_2], many=True).data
        expected_data = [
            {
                "id": book_1.id,
                "name": "test book 1",
                "price": "25.00",
                "author_name": "test author 1"
            },
            {
                "id": book_2.id,
                "name": "test book 2",
                "price": "55.00",
                "author_name": "test author 2"
            }
        ]
        self.assertEqual(data, expected_data)
