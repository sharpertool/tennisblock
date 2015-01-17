#!/bin/bash

dbname=$1

if [ -z "$dbname"   ]
then
    echo "Enter a db name"
    exit 1
fi

echo "drop database if exists $dbname ;" | mysql
echo "CREATE DATABASE $dbname CHARACTER SET utf8 COLLATE utf8_general_ci;" | mysql
echo "grant all on \`$dbname\`.* to tennisblock@localhost;" | mysql


