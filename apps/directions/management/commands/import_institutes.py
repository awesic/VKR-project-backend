import json

from django.core.management import BaseCommand

from config import settings
from apps.directions.models import Institute


class Command(BaseCommand):
    help = "Import institutes from json file"

    def handle(self, *args, **options):
        file_path = settings.BASE_DIR / 'data' / 'institutes.json'
        with open(file_path) as file:
            data = json.load(file)
            for data_object in data:
                id = data_object.get('id')
                label = data_object.get('label')
                fullname = data_object.get('fullname')
                try:
                    institute, created = Institute.objects.get_or_create(id=id, label=label, fullname=fullname)
                    if created:
                        institute.save()
                        print(f'\n{institute} was created')
                except Exception as e:
                    print(str(e))
                    print(f'Something went wrong while importing: {id}')