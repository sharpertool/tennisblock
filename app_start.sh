#!/bin/bash

pushd ~/proj/gardentronic/gardentronic/nginx_dev 
sudo start.sh
popd

dc up -d

tmux split-window 'cd webpack_assets && yarn watch'
tmux split-window 'cd client && yarn hots'

./runserver -c




