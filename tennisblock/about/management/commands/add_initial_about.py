from django.core.management.base import BaseCommand
from wagtail.core.models import Page

from textwrap import dedent

from about.models import About


class Command(BaseCommand):
    args = ''
    help = dedent('''
        Add a new About Page, if one does not exist
''')

    def handle(self, *args, **options):

        if not About.objects.all().exists():
            root = Page.objects.get(pk=2)
            page = About(
                title='About Us',
                intro="<b>We build tools to schedule tennis</b>",
                slug='about-us'
            )
            root.add_child(instance=page)
            page.save_revision().publish()



