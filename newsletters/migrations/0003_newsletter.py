# Generated by Django 3.2 on 2022-08-26 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletters', '0002_auto_20220825_1425'),
    ]

    operations = [
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=255)),
                ('body', models.TextField()),
                ('status', models.CharField(choices=[('Draft', 'Draft'), ('Published', 'Published')], max_length=10)),
                ('create', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('email', models.ManyToManyField(to='newsletters.NewsletterUsers')),
            ],
        ),
    ]