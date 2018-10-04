#!/bin/bash

zipfile=$1
VERSION=$2
APPPATH=${APPPATH:-/var/www/tennisblock}
zipdir=/home/ubuntu/zipdir
excludefile=/home/ubuntu/tennisblock_exlude.lst

# Put site into maintenance mode
touch ${APPPATH}/maintenance.on

echo "unzip ${zipfile} to ${zipdir}"
rm -rf ${zipdir}
mkdir -p ${zipdir}
mkdir -p ~/deploy
pushd ${zipdir}
unzip -uoq ~/deploy/${zipfile}
popd

cd ${APPPATH}

echo "use rsync to synchronize the two paths"
sudo -u django rsync -av --delete --exclude-from ${excludefile} ${zipdir}/ .
if [ $? -ne 0 ];then
    echo "Rsync failed.. abandoning update"
    exit 2
fi

echo "Update requirements"
.venv3/bin/pip install -r requirements/prod.txt

#echo -e "\n Collecting updated statics.."
#./manage collectstatic --noinput

# Show any pending migrations
./manage showmigrations | grep "\[ \]\|^[a-z]" | grep "[ ]" -B 1

# Run migrations
./manage migrate --noinput

echo "Updating APP_VERSION to match production version"
template_version=$(grep APP_VERSION sharpertool/production.env.j2  | sed 's/APP_VERSION=//')
sed -i -e "s/APP_VERSION=.*/APP_VERSION=${VERSION}/" .env

# Update app directory user and group values
sudo chown -R django:www-data ${APPPATH}

echo -e "\n Reloading uWSGI web service.."

# Reload with reload.me
touch ${APPPATH}/reload.me

rm ${APPPATH}/maintenance.on

