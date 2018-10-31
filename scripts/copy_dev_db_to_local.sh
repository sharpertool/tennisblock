#!/usr/bin/env bash

server=localhost
dt=$(date '+%Y-%M-%d-%H_%M')
filename="tennisblock_db_${dt}.sql"
echo "Dumping to filename ${filename}"

ssh gb "pg_dump -h ${server} -U tennisblock tennisblock > ${filename}"
scp gb:${filename} database/backups
ssh gb "rm ${filename}"

