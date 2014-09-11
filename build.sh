#!/bin/bash

arfile='tennisblock_dev.zip'
ardest='../tennisblock-deploy'

echo "Cleaning up.."
rm -f $arfile
mkdir -p $ardest

if [ -d $ardest ];then
    rm -rf $ardest/currentVersion
    rm  $ardest/$arfile
fi

echo "Building..."

# Build less compiled files and additional javascript libraries.
build/build.py

# Collect static files
python manage.py setting:build collectstatic --clear --noinput

# Combine all of the required artifacts into a zip file.
build/buildArchive.py --gz $arfile

echo "Installing..."
mv $arfile $ardest
pushd $ardest
unzip -q -o $arfile -d currentVersion
touch wsgi.py
popd
