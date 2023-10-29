# Generated by Django 4.2.6 on 2023-10-27 10:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('book', '0003_alter_book_isbn'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Peminjaman',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tanggal_peminjaman', models.DateField(auto_now_add=True)),
                ('tanggal_pengembalian', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('dipinjam', 'Dipinjam'), ('dikembalikan', 'Dikembalikan')], max_length=255)),
                ('buku', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.book')),
                ('pengguna', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]