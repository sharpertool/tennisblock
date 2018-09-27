#!/usr/bin/env bash

server=localhost
dt=$(date '+%Y-%M-%d-%H_%M')
filename="tennisblock_demo_db_${dt}.sql"
echo "Dumping to filename ${filename}"

ssh gb "pg_dump -h ${server} -U django_user tennisblock > ${filename}"
scp gb:${filename} database/backups
ssh gb "rm ${filename}"

