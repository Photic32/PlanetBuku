# Generated by Django 4.2.4 on 2023-10-28 17:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("book", "0004_auto_20231028_2339"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Peminjaman",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("tanggal_peminjaman", models.DateField(auto_now_add=True)),
                ("tanggal_pengembalian", models.DateField(null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("dipinjam", "Dipinjam"),
                            ("dikembalikan", "Dikembalikan"),
                        ],
                        max_length=255,
                    ),
                ),
                (
                    "buku",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="book.book"
                    ),
                ),
                (
                    "pengguna",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Peminjam",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("jumlah_buku_dipinjam", models.IntegerField(default=0)),
                ("peminjaman_list", models.ManyToManyField(to="home.peminjaman")),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Keranjang",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("jumlah_buku", models.IntegerField(default=0)),
                ("book_list", models.ManyToManyField(null=True, to="book.book")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
