#!/bin/bash
# stop on errors
set -e

# we might run into trouble when using the default `postgres` user, e.g. when dropping the postgres
# database in restore.sh. Check that something else is used here
if [ "$POSTGRES_USER" == "postgres" ]
then
    echo "creating a backup as the postgres user is not supported, make sure to set the POSTGRES_USER environment variable"
    exit 1
fi

# Set the default database to be the username
: ${POSTGRES_DB:=$POSTGRES_USER}
export POSTGRES_DB

# export the postgres password so that subsequent commands don't ask for it
export PGPASSWORD=$POSTGRES_PASSWORD

echo "creating backup"
echo "---------------"

# Calculate a default filename
DEFAULT=backup_$(date +'%Y_%m_%dT%H_%M_%S').sql
if [ -z "$1" ]
then
	FILENAME=${DEFAULT}
	echo "Using default filename"
else
	FILENAME=${1}_$(date +'%Y_%m_%dT%H_%M_%S').sql
	echo "Used user-defined filename prefix ${1}"
fi

if [[ $(dirname ${FILENAME}) == '.' ]];then
    FILENAME=/backups/$(basename ${FILENAME})
fi
echo "Full backup filename ${FILENAME}"
echo "User: $POSTGRES_USER DB: $POSTGRES_DB"

pg_dump -h postgres -U $POSTGRES_USER $POSTGRES_DB >> $FILENAME

echo "successfully created backup $FILENAME"
echo $FILENAME

