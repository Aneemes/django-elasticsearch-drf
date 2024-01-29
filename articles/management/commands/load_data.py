import json
from django.core.management.base import BaseCommand
from articles.models import Category, Article  # replace 'yourapp' with the actual name of your Django app

class Command(BaseCommand):
    help = 'Load data from JSON file into Django models'

    def handle(self, *args, **options):
        with open('demo-data.json') as file:
            data = json.load(file)

            categories = data.get('categories', [])
            articles = data.get('articles', [])

            for category_data in categories:
                Category.objects.create(**category_data)

            for article_data in articles:
                category_title = article_data.pop('category')
                category = Category.objects.get(title=category_title)
                Article.objects.create(category=category, **article_data)

        self.stdout.write(self.style.SUCCESS('Data loaded successfully.'))
