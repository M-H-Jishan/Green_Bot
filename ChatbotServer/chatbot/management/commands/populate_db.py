from django.core.management.base import BaseCommand
from chatbot.models import Category, Intent, KnowledgeBase
import json

class Command(BaseCommand):
    help = 'Populate the database with initial data'

    def add_arguments(self, parser):
        parser.add_argument('--data-file', type=str, help='Path to JSON data file')

    def handle(self, *args, **options):
        data_file = options['data_file']
        if not data_file:
            self.stdout.write(self.style.ERROR('Please provide a data file path'))
            return

        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Create categories
            self.stdout.write('Creating categories...')
            categories = {}
            for cat_data in data.get('categories', []):
                category = Category.objects.create(
                    name=cat_data['name'],
                    description=cat_data.get('description', ''),
                    parent_id=categories.get(cat_data.get('parent'), None)
                )
                categories[cat_data['name']] = category.id
            self.stdout.write(self.style.SUCCESS(f'Created {len(categories)} categories'))

            # Create intents
            self.stdout.write('Creating intents...')
            intents = {}
            for intent_data in data.get('intents', []):
                intent = Intent.objects.create(
                    name=intent_data['name'],
                    description=intent_data.get('description', ''),
                    keywords=','.join(intent_data.get('keywords', []))
                )
                intents[intent_data['name']] = intent.id
            self.stdout.write(self.style.SUCCESS(f'Created {len(intents)} intents'))

            # Create knowledge base entries
            self.stdout.write('Creating knowledge base entries...')
            kb_count = 0
            for kb_data in data.get('knowledge_base', []):
                entry = KnowledgeBase.objects.create(
                    question=kb_data['question'],
                    answer=kb_data['answer'],
                    category_id=categories.get(kb_data.get('category')),
                    intent_id=intents.get(kb_data.get('intent')),
                    source_url=kb_data.get('source_url'),
                    priority=kb_data.get('priority', 0),
                    context_data=kb_data.get('context_data', {})
                )
                kb_count += 1

            self.stdout.write(self.style.SUCCESS(f'Created {kb_count} knowledge base entries'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
