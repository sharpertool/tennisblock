from os.path import *

directory_specifications = {
    'dev': {
        'dirs': [
        ],
        'patterns': [
        ]
    },
    'prod': {
        'files': [
            'requirements.txt',
            'virtual_update.sh',
            'run_migrations.sh',
            'favicon.png',
            'favicon.ico'
        ],
        'dirs': {
            'schematics/backend_api': {},
            'schematics/component_api': {},
            'schematics/editor': {},
            'schematics/embed': {},
            'schematics/locale': {},
            'schematics/projects': {},
            'schematics/PSLib': {},
            'schematics/settings': {
                'ignore': ['.*local_settings.*']
            },
            'schematics/site_media': {},
            'schematics/templates': {},
            'schematics/management': {},
            'schematics/migrations': {},
            'collectedstatic': { 'ignore' : '.*/eeweb/.*'},
            'schematics': {
                'files': '*.py',
                'recursive': False,
                'ignore': ['.*wsgi.*','local_settings.*']
            },
            'webapp_api': {},
            '.': {
                'files': [
                    'manage.py',
                ],
                'recursive': False
            }
        },
        'globalignore': [
            r'\.git/',
            r'\.pyc$',
            join("utilities", 'batik', 'samples'),
            join("utilities", 'batik', 'docs'),
            r"mxClientDebug.js",
            r"local_settings.py"
        ]
    }
}
