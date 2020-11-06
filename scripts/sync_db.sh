#!/bin/bash

cd ~/proj/sharpertool/tennis_home/tennisblock
source .envrc
source .env
export PATH=$PATH:/usr/local/bin
/usr/local/bin/docker-compose exec -T postgres backup


