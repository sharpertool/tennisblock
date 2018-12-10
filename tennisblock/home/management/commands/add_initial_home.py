from django.core.management.base import BaseCommand
from wagtail.core.models import Page

from textwrap import dedent

from home.models import Home


class Command(BaseCommand):
    args = ''
    help = dedent('''
        Add a new Home Page, if one does not exist
''')

    def handle(self, *args, **options):

        if not Home.objects.all().exists():
            root = Page.objects.get(pk=2)
            my_home = Home(
                title='Welcome to Tennis Block',
                intro="<b>We can schedule your tennis life</b>",
                slug='home'
            )
            root.add_child(instance=my_home)
            my_home.save_revision().publish()



