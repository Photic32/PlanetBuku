from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from view_book.models import Review
from book.models import Book
from home.models import Keranjang
from django.urls import reverse

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='Aza',
            password='semangat'
        )
        self.book = Book.objects.create(
            title='Dummy Title',
            author='Lorem Ipsum',
            publication_year=2021,
            publisher='PBP',
            stock=5
        )
        self.keranjang = Keranjang.objects.create(user=self.user)

    def test_view_books(self):
        url = reverse('view_book:view_books')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_books.html')

    def test_view_book_detail(self):
        url = reverse('view_book:single_book_view', args=[self.book.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_detail.html')
    
    def test_view_book_detail_authenticated(self):
        self.client.login(username='Aza', password='semangat')
        url = reverse('view_book:single_book_view', args=[self.book.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_detail.html')

    def test_search_books_view(self):
        url = reverse('view_book:search_books')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_books.html') 

    def test_search_books_with_query(self):
        url = reverse('view_book:search_books')
        response = self.client.get(url, {'q': 'Test Book'})
        self.assertEqual(response.status_code, 200)

    def test_add_to_cart_ajax(self):
        url = reverse('view_book:add_to_cart_ajax', args=[self.book.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 201)

    def test_get_review_json(self):
        url = reverse('view_book:get_review_json', args=[self.book.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_give_review_ajax(self):
        url = reverse('view_book:give_review_ajax', args=[self.book.pk])
        review = {
            'review': 'Test review',
            'rate': 4,
        }
        response = self.client.post(url, review)
        self.assertEqual(response.status_code, 201)

class ReviewModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        book = Book.objects.create(title='Test Book', author='Test Author')
        user = User.objects.create_user(
            username='Aza',
            password='semangat'
        )
        Review.objects.create(
            book=book,
            user=user,
            review='Test Review',
            rate=4
        )

    def test_review_fields(self):
        review = Review.objects.get(id=1)
        self.assertEqual(review.book.title, 'Test Book')
        self.assertEqual(review.user.username, 'Aza')
        self.assertEqual(review.review, 'Test Review')
        self.assertEqual(review.rate, 4)