import json

from django.core.management import BaseCommand

from config import settings
from apps.directions.models import Direction, Institute


class Command(BaseCommand):
    help = 'Import directions from json file'

    def handle(self, *args, **options):
        file_path = settings.BASE_DIR / 'data' / 'directions.json'
        with open(file_path) as file:
            data = json.load(file)
            for data_object in data:
                id = data_object.get('id')
                label = data_object.get('label')
                institutes = data_object.get('institutes')
                try:
                    direction, created = Direction.objects.get_or_create(id=id, label=label)
                    if created:
                        direction.save()
                        print(f'\n{direction} was created')
                    for institute in institutes:
                        direction.institutes.add(Institute.objects.get(id=institute))
                        print(f'institutes {institutes} added to {direction}')
                except Exception as e:
                    print(str(e))
                    print(f'Something went wrong while importing: {id} {label}')
