#!/bin/bash

apps="schematics aspeni18ndb schematicdb"

for app in $apps
do
    echo "Syncing $app"
    python manage.py schemamigration $app --initial
    python manage.py migrate $app --fake
done

