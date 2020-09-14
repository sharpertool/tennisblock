#!/bin/bash

s3path=$1
zipfile=$2
apppath=${APPPATH:-"/home/django/gardenbuzz"}

# Put site into maintenance mode
touch ${apppath}/maintenance.on

cd ${apppath}

echo "Pulling latest code updates.."
/usr/local/bin/aws s3 cp ${s3path}/${zipfile} .

unzip -uo ${zipfile}
rm ${zipfile}

# We need to be able to control which one of these runs.
.venv3/bin/pip install -r requirements/prod.txt

echo -e "\n Collecting updated statics.."
./manage collectstatic --noinput

# Show any pending migrations
./manage showmigrations | grep "\[ \]\|^[a-z]" | grep "[ ]" -B 1

# Run migrations
./manage migrate --noinput

echo -e "\n Reloading uWSGI web service.."
touch reload.me

rm ${apppath}/maintenance.on

