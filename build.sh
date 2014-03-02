#!/bin/bash

arfile='schematics.com_dev.zip'
ardest='../schematics.com-deploy'

echo "Cleaning up.."
rm -f $arfile
mkdir -p $ardest
rm -rf $ardest/currentVersion
rm  $ardest/$arfile

echo "Building..."

# Build less compiled files and additional javascript libraries.
build/build.py

# Collect static files
python manage.py collectstatic --clear --noinput --ignore eeweb

# Combine all of the required artifacts into a zip file.
build/buildArchive.py --gz $arfile

echo "Installing..."
mv $arfile $ardest
pushd $ardest
unzip -q -o $arfile -d currentVersion
touch wsgi.py
popd
