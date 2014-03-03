"""
WSGI config for schematics project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os
import sys
import site

sitepath = os.environ.get('SITEPATH',"/home/ec2-user/Envs/tennisblock-dev/")
pythonversion = os.environ.get('PYTHONVERSION','python2.7')
#virtualenv:schematics.com-dev
sitelib = os.path.join(sitepath,'lib',pythonversion,'site-packages')

site.addsitedir(sitelib)

print("Using sitedir %s" % sitelib)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tennisblock.settings.test")

activate_env=os.path.join(sitepath,"bin/activate_this.py")
execfile(activate_env,dict(__file__=activate_env))

print("Running startup..")
import tennisblock.startup as startup
startup.run()
print("Done with startup")

import tennisblock.monitor as monitor
monitor.start(interval=1.0)
monitor.track(__file__)

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
