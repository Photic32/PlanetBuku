# Generated by Django 4.2.4 on 2023-10-29 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daftar_peminjam', '0005_remove_peminjam_pengembalian_paling_awal_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='peminjam',
            name='book_list',
            field=models.ManyToManyField(blank=True, to='daftar_peminjam.peminjaman'),
        ),
    ]
