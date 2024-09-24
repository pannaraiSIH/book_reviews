# Generated by Django 5.1.1 on 2024-09-20 19:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=100)),
                ('publication_date', models.DateField()),
                ('genre', models.CharField(choices=[('fiction', 'Fiction'), ('non-fiction', 'Non-Fiction'), ('mystery', 'Mystery'), ('fantasy', 'Fantasy'), ('Biology', 'Biology')], max_length=50)),
                ('description', models.TextField()),
                ('cover_image', models.BinaryField()),
                ('created', models.DateTimeField(auto_now=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('create_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='books_created', to=settings.AUTH_USER_MODEL)),
                ('update_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='books_updated', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]