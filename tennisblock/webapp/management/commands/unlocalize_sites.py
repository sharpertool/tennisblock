import re
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from wagtail.core.models import Site


class Command(BaseCommand):
    help = 'Convert a localized DB back to run on dev server'

    def add_arguments(self, parser):
        parser.add_argument('--port', type=int, default=443)

    def handle(self, *args, **options):
        newport = options.get('port')
        sites = Site.objects.all()

        # Get the first site, make sure it's gardenbuzz.local
        site = Site.objects.all()[0]
        site.domain = 'tennisblock.com'
        site.name = 'TennisBlock'
        site.save()

        for site in sites:
            newhost = re.sub(r'\.local', '.com', site.hostname)
            if newhost != site.hostname or site.port != newport:
                print(f"Updating {site.hostname} to {newhost} and Port from {site.port} to {newport}")
                site.hostname = newhost
                site.port = newport
                site.save()



