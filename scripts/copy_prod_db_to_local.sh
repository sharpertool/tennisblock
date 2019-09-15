#!/usr/bin/env bash

server=localhost
dt=$(date '+%Y-%m-%d-%H_%M')
filename="tennisblock_prod_db_${dt}.sql"
backup_path=~/DropboxST/SharperToolDev/database/tennisblock/
full_filename=${backup_path}/${filename}
echo "${full_filename}"

#ls -al ${backup_path}
# Can can do this all in one command!
ssh tb "sudo -u postgres pg_dump tennisblock" > ${full_filename}


