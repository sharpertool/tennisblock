#!/bin/bash

env=$(egrep \#virtualenv wsgi.py | sed 's/#virtualenv:\(\S*\)/\1/')

if [ -z "$env" ];then
	echo "Failed to find the virtualenv "
	exit
fi

echo "Updating virtual environment $env"

if [ -z "$WORKON_HOME" ]; then
	export WORKON_HOME=/opt/python/virtualenvs
fi

if [ -f "/usr/local/bin/virtualenvwrapper.sh" ];then
	source /usr/local/bin/virtualenvwrapper.sh
elif [ -f "/usr/bin/virtualenvwrapper.sh" ];then
	source /usr/bin/virtualenvwrapper.sh
else
	echo "Please install virtualenvwrapper!!"
	echo ">sudo pip install virtualenvwrapper"
fi

echo "Adding/Updating any python modules"
workon $env
if [ -f 'currentVersion/requirements.txt' ];then
	pip install -r currentVersion/requirements.txt
fi


