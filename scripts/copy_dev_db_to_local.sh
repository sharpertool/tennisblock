#!/usr/bin/env bash

server=localhost
dt=$(date '+%Y-%m-%d-%H_%M')
filename="tennisblock_demo_db_${dt}.sql"
set -o allexport
source .env
set +o allexport

backup_path=$(cat docker-compose.yml \
    | yq -r '.services.postgres.volumes[] | select(test("/backups$")) | split(":")[0]')
#backup_path=~/Dropbox/GardenbuzzDev/Development/database/backups
echo "Extracted backup path as ${backup_path} from docker-compose.yml"
eval full_filename=${backup_path}/${filename}
echo "Dumping to filename ${full_filename}"

ssh tb "pg_dump -h ${server} -U tennisblock tennisblock"  > "${full_filename}"

