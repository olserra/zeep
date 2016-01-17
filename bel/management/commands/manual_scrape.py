from django.core.management.base import BaseCommand
from bel.utils import pagination


class Command(BaseCommand):
    def handle(self, *args, **options):
        pagination()
