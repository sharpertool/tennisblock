#!/usr/bin/env bash

host="Host deploy_host"
nm="Hostname ${DEPLOY_HOST}"
user="User ubuntu"
strict="StrictHostKeyChecking no"

mkdir -p ~/.ssh
echo -e "Host deploy_host\n" >> ~/.ssh/config
echo -e "    StrictHostKeyChecking no\n\n" >> ~/.ssh/config
echo -e "    ${nm}\n\n" >> ~/.ssh/config
echo -e "    ${user}\n" >> ~/.ssh/config

cat ~/.ssh/config




