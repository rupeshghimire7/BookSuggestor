# Generated by Django 4.1.5 on 2023-01-24 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0012_alter_book_photo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={},
        ),
        migrations.RemoveField(
            model_name='book',
            name='created_at',
        ),
    ]
