from django.core.management.base import BaseCommand
from bel.utils import process_koop


class Command(BaseCommand):
    def handle(self, *args, **options):
        process_koop()
