from django.core.management.base import BaseCommand 

from example.models import Member 

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('name')
        parser.add_argument('region', choices=['NA', 'EU'])
        parser.add_argument('--moderator', action='store_true')

    def handle(self, *args, **options):
        member = Member(
            name=options['name'], 
            region=options['region'],
            moderator=options['moderator']
            )
        member.save()
        self.stdout.write(self.style.SUCCESS('Added member!'))