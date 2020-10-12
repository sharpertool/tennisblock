#!/bin/bash

VENVBASE=/home/ec2-user/Envs
VENV=${VENVBASE}/$1

if [ -z "$VENV" ];then
    #echo "Usage: runinenve [virutalenv_path] CMDS"
    echo "Usage: supervisord_launcher.sh [virtualenv path] COMMANDS"
    exit 1
fi

. ${VENV}/bin/activate

shift 1
echo "Executing $@ in ${ENV}"
exec "$@"

deactivate
