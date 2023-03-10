# Generated by Django 4.1.4 on 2023-01-02 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_genre_books'),
    ]

    operations = [
        migrations.RenameField(
            model_name='books',
            old_name='book',
            new_name='name',
        ),
        migrations.AddField(
            model_name='books',
            name='author',
            field=models.ManyToManyField(to='books.author'),
        ),
        migrations.AddField(
            model_name='books',
            name='rating',
            field=models.FloatField(default=0.0),
        ),
    ]
