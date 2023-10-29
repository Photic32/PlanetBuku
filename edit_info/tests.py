from django.test import TestCase
from django.urls import reverse
from .models import Peminjam, Peminjaman
from book.models import Book
from django.contrib.auth.models import User

class PeminjamTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.peminjam = Peminjam.objects.create(user=self.user, jumlah_buku_dipinjam=2)
        self.book = Book.objects.create(title='Test Book', author='Test Author')
        self.peminjaman = Peminjaman.objects.create(pengguna=self.user, buku=self.book, tanggal_pengembalian='2039-01-01', status='dipinjam')

    def test_serialize_semua_peminjam(self):
        response = self.client.get(reverse('daftar_peminjam:get_all_user_json'))
        self.assertEqual(response.status_code, 200)

    def test_get_pinjaman_json(self):
        response = self.client.get(reverse('daftar_peminjam:get_pinjaman_json', args=[self.peminjaman.id]))
        self.assertEqual(response.status_code, 200)

    def test_show_peminjam_individu(self):
        response = self.client.get(reverse('daftar_peminjam:show_peminjam_individu', args=[self.peminjam.id]))
        self.assertEqual(response.status_code, 200)

    def test_show_page(self):
        response = self.client.get(reverse('daftar_peminjam:show_page'))
        self.assertEqual(response.status_code, 200)

    def test_edit_peminjaman(self):
        response = self.client.post(reverse('daftar_peminjam:edit_peminjaman', args=[self.peminjaman.id]), {'tanggal_pengembalian': '2039-12-12'})
        self.assertEqual(response.status_code, 200)
        self.peminjaman.refresh_from_db()
        self.assertEqual(str(self.peminjaman.tanggal_pengembalian), '2039-12-12')

    def test_kembali_buku(self):
        response = self.client.get(reverse('daftar_peminjam:kembali_buku', args=[self.peminjaman.id]))
        self.assertEqual(response.status_code, 200)
        self.peminjaman.refresh_from_db()
        self.assertEqual(self.peminjaman.status, 'dikembalikan')

    def test_search_buku(self):
        params = {
            "title": "Test",
            "author": "Test Author",
            "isbn": "",
            "year": "",
            "publisher": "",
            "user_id": self.peminjam.id
        }
        response = self.client.get(reverse('daftar_peminjam:search_buku'), params)
        self.assertEqual(response.status_code, 200)
