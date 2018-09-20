#!/bin/bash

if [ -z "${DATAPAGES_ROOT}" ];then
    echo "Please set the DATAPAGES_ROOT environment variable to point to your datapages.io directory"
    exit 2
fi

scripts=$(cd $(dirname $0);pwd)
base=${scripts}/..

frontend=${DATAPAGES_ROOT}/django_root/frontend

rsync -av --exclude webpack-stats.json ${base}/dist.prod/ ${frontend}/static
cp ${base}/dist.prod/webpack-stats.json ${frontend}
