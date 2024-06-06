import json
from django.core.management.base import BaseCommand
from django.urls import get_resolver

class Command(BaseCommand):
    help = 'List all URLs in the project'

    def handle(self, *args, **kwargs):
        url_patterns = get_resolver().url_patterns
        urls = []

        def extract_urls(patterns, base=''):
            for pattern in patterns:
                if hasattr(pattern, 'url_patterns'):
                    extract_urls(pattern.url_patterns, base + pattern.pattern.regex.pattern)
                else:
                    url = {
                        'pattern': base + pattern.pattern.regex.pattern,
                        'name': pattern.name
                    }
                    urls.append(url)

        extract_urls(url_patterns)

        with open('static/api/endpoints.json', 'w') as f:
            json.dump(urls, f, indent=4)

        self.stdout.write(self.style.SUCCESS('Successfully generated endpoints.json'))