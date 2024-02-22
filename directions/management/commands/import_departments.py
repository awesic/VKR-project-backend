import json

from django.core.management import BaseCommand

from config import settings
from directions.models import Department, Institute


class Command(BaseCommand):
    help = 'Import departments from json file'

    def handle(self, *args, **options):
        file_path = settings.BASE_DIR / 'data' / 'departments.json'
        with open(file_path) as file:
            data = json.load(file)
            for data_object in data:
                label = data_object.get('label')
                institute = data_object.get('institute')
                try:
                    department, created = Department.objects.get_or_create(label=label, institute=Institute.objects.get(id=institute))
                    if created:
                        department.save()
                        print(f'\n{department} was created')
                except Exception as e:
                    print(str(e))
                    print(f'Something went wrong while importing: {label}')
