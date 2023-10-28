from typing import Any
from django.db.models.query import QuerySet
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
from django.utils.timezone import datetime
from django.db import models
from book.models import Book
from django.contrib.auth.models import User, UserManager, AbstractBaseUser, PermissionsMixin, AbstractUser, BaseUserManager
#from view_book.models import Review

# class Book(models.Model): # App 2
#     isbn = models.TextField(null=True, blank=True)
#     title = models.TextField(null=True, blank=True)
#     author = models.TextField(null=True, blank=True)
#     publication_year = models.IntegerField(null=True, blank=True)
#     publisher = models.TextField(null=True, blank=True)
#     image_s = models.TextField(null=True, blank=True)
#     image_m = models.TextField(null=True, blank=True)
#     image_l = models.TextField(null=True, blank=True)
#     stock = models.IntegerField(null=True, blank=True)

# class Review(models.Model): # App 3
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     review = models.TextField()
#     rate = models.IntegerField()
#     review_date = models.DateField(auto_now_add=True)

class Keranjang(models.Model): # App 4
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book_list = models.ManyToManyField(Book)
    jumlah_buku = models.IntegerField(default=0)
    
class Peminjaman(models.Model): # App 5
    pengguna = models.ForeignKey(User, on_delete=models.CASCADE)
    tanggal_peminjaman = models.DateField(auto_now_add=True)
    tanggal_pengembalian = models.DateField(null=True)
    buku = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=[('dipinjam', 'Dipinjam'), ('dikembalikan', 'Dikembalikan')])

    def save(self, *args, **kwargs):
        if self.tanggal_pengembalian is None:
            self.tanggal_pengembalian = self.tanggal_peminjaman.date() + datetime.timedelta(days=7)
        super(Peminjaman, self).save(*args, **kwargs)

class Peminjam(models.Model): # App 1
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    peminjaman_list = models.ManyToManyField(Peminjaman)
    jumlah_buku_dipinjam = models.IntegerField(default=0)


# class User(AbstractUser):
#     class Role(models.TextChoices):
#         ADMIN = "ADMIN", 'Admin'
#         STAF = "STAF", 'Staf'
#         CUSTOMER = "CUSTOMER", 'Customer'

#     base_role = Role.ADMIN

#     role = models.CharField(max_length=50, choices=Role.choices)

#     def save(self, *args, **kwargs):
#         if not self.pk:
#             self.role = self.base_role
#         return super().save(*args, **kwargs)

# class StafManager(BaseUserManager):
#     def get_queryset(self, *args, **kwargs):
#         res = super().get_queryset(*args, **kwargs)
#         return res.filter(role = User.Role.STAF)

# class Staf(User):

#     base_role = User.Role.STAF

#     staf = StafManager()

#     class Meta:
#         proxy = True

# class CustomerManager(BaseUserManager):
#     def get_queryset(self, *args, **kwargs):
#         res = super().get_queryset(*args, **kwargs)
#         return res.filter(role = User.Role.CUSTOMER)

# class Customer(User):

#     base_role = User.Role.CUSTOMER

#     staf = CustomerManager()

#     class Meta:
#         proxy = True

# class CustomUserManager(UserManager):
#     def _create_user(self, email, password, **extra_fields):
#         if not email:
#             raise ValueError("Bukan E-Mail Valid")
#         email = self.normalize_email(email)
#         user = self.model(email= email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)

#         return user
    
#     def create_user(self, email=None, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', False)
#         extra_fields.setdefault('is_superuser', False)
#         return self._create_user(email, password, **extra_fields)
    
#     def create_superuser(self, email=None, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self._create_user(email, password, **extra_fields)
    
# class User(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(blank=True, default='', unique=True)
#     name = models.CharField(max_length=255, blank=True, default='')

#     is_active = models.BooleanField(default=True)
#     is_superuser = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)

#     date_joined = models.DateTimeField(default=timezone.now)
#     last_login = models.DateTimeField(blank=True, null=True)

#     objects=CustomUserManager()

#     USERNAME_FIELD='email'
#     EMAIL_FIELD='email'
#     REQUIRED_FIELDS = []

#     class meta:
#         verbose_name = 'User'
#         verbose_name_plural = 'Users'

#     def get_full_name(self):
#         return self.name
    
#     def get_short_name(self):
#         return self.name
        
