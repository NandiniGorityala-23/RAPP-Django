from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Creating groups at initial stage'
    group_names = ["RMG", "HR", "PM"]

    def handle(self, *args, **options):
        for name in self.group_names:
            new_group, created = Group.objects.get_or_create(name=name)
        print"%s Groups created successfully" % ", ".join(self.group_names)