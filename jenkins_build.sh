#!/bin/bash

# This script is used to build the deploy product on the jenkins server
# I create a virtual environment if one does not exist.
# Use pip to setup teh requirements. All of this is just so that we
# can use collectstatic to pull all of the static files onto a single dir..

# Once we get all of the static files collected, we

if [ $# -ge 2 ]
then
    vmname=$1
    zipfile=$2
else
    echo "Required arguments missing. Usage: jenkins_build.sh virtualenv_name zipname"
    exit 2
fi


export WORKON_HOME=/opt/envs

echo "Setup WORKON_HOME to $WORKON_HOME/$vmname"
mkdir -p $WORKON_HOME

echo "Source the wrapper"
if [[ -f '/usr/bin/virtualenvwrapper.sh' ]];then
    . /usr/bin/virtualenvwrapper.sh
elif [[ -f '/usr/local/bin/virtualenvwrapper.sh' ]];then
    . /usr/local/bin/virtualenvwrapper.sh
else
    echo "Could not find virtualenvironment wrapped."
    exit 3
fi

echo "Check the virtual environment."
if [[ ! -d "$WORKON_HOME/$vmname" ]];then
    echo "Building new VM:$vmname"
    mkvirtualenv $vmname
else
    echo "VM Already existed.."
    workon $vmname
fi


echo "Working on $vmname"
workon $vmname
# Update the requirements
# Patch the requirements for jenkins..
# I've never been able to resolve this MySQL-python install bug that occurs on the jenkins server.
#cat requirements.txt | sed 's/MySQL-python==1.2.4/mysql-python/' > jenkins_requirements.txt
#pip install --allow-all-external --allow-insecure PIL -r jenkins_requirements.txt
pip install -r requirements.txt

# Build less compiled files and additional javascript libraries.
build/build.py

# Collect static files
python manage.py settings:build collectstatic --noinput

# Combine all of the required artifcats into a zip file.
build/buildArchive.py --gz $zipfile

