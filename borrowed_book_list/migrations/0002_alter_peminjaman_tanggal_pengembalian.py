# Generated by Django 4.2.4 on 2023-10-29 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('borrowed_book_list', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='peminjaman',
            name='tanggal_pengembalian',
            field=models.DateField(),
        ),
    ]
