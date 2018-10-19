#!/usr/bin/env bash

server=localhost
filename=$1

if [[ -z "$filename" ]]
then
    echo "You must enter a valid filename"
    exit 2
fi

backup_path=~/Dropbox/GardenbuzzDev/Development/database/backups
full_filename=${backup_path}/${filename}

if [[ ! -e $full_filename ]]
then
    echo "Filename specified does not exist"
    exit 2
fi

echo "Restore ${full_filename} to dev server"

scp ${full_filename} gb:/tmp/${filename}
ssh gb.root "sudo -u postgres dropdb gardenbuzz"
ssh gb.root "sudo -u postgres createdb gardenbuzz -O django_user"
ssh gb.root "sudo -u postgres psql -U django_user -d gardenbuzz < /tmp/${filename}"
ssh gb "rm /tmp/${filename}"
ssh gb "cd gardenbuzzz && ./manage unlocalize_sites"


