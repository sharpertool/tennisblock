#!/bin/bash

scripts=$(cd $(dirname $0);pwd)
base=${scripts}/..

frontend=${base}/../tennisblock/frontend

rsync -av --exclude webpack-stats.json ${base}/dist.prod/ ${frontend}/static
cp ${base}/dist.prod/webpack-stats.json ${frontend}
