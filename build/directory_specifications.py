from os.path import *

directory_specifications = {
    'prod': {
        'files': [
            'requirements.txt',
            'virtual_update.sh',
            'run_migrations.sh',
            #'favicon.png',
            #'favicon.ico'
        ],
        'dirs': {
            'tennisblock/accounts': {},
            'tennisblock/api': {},
            'tennisblock/blockdb': {},
            'tennisblock/members': {},
            'tennisblock/mixins': {},
            'tennisblock/sekizai_processors': {},
            'tennisblock/settings': {
                'ignore': ['.*local_settings.*']
            },
            'tennisblock/static': {},
            'tennisblock/TBLib': {},
            'tennisblock/templates': {},
            'tennisblock/templatetags': {},
            'tennisblock/tools': {},
            #'collectedstatic': { 'ignore' : '.*/pat/.*'},
            'collectedstatic': { },
            'tennisblock': {
                'files': '*.py',
                'recursive': False,
                'ignore': ['.*wsgi.*','local_settings.*']
            },
        },
        'globalignore': [
            r'\.git/',
            r'\.pyc$',
            r"local_settings.py"
        ]
    }
}
