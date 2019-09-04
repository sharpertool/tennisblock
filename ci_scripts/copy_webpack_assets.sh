#!/bin/bash

scripts=$(cd $(dirname $0);pwd)
base=${scripts}/..
build=${base}/webpack_assets

frontend=${base}/tennisblock/frontend

rsync -av --exclude webpack-assets-stats.json --exclude js/ ${build}/dist.prod/ ${frontend}/static
cp ${build}/dist.prod/webpack-assets-stats.json ${frontend}
