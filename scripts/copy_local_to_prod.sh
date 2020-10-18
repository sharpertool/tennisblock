#!/usr/bin/env bash

scripts=$(cd $(dirname $0);pwd)
root=$(cd $(dirname $0);cd ..;pwd)

file=$1

if [ -z $file ];then
  echo "Must provide full path to a file to restore"
  exit 2
fi

if [ ! -f $file ];then
  echo "Missing file $file"
  exit 3
fi

# Remove existing file, if it exists
ssh tb "sudo rm /tmp/$(basename $file)"

# copy file to tmp location
scp $file tb:/tmp/$(basename $file)

# Restore the file
ssh tb "sudo -u postgres psql --dbname=tennisblock -f /tmp/$(basename $file)"

# Remote from temp for cleanup
ssh tb "sudo rm /tmp/$(basename $file)"

