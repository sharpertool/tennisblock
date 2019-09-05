#!/usr/bin/env bash

target_host=$1
echo "Target Host: ${target_host}"

host="Host deploy_host"
nm="  Hostname ${target_host}"
user="User ubuntu"
strict="  StrictHostKeyChecking no"

mkdir -p ~/.ssh
echo -e "Host deploy_host\n" >> ~/.ssh/config
echo -e "    StrictHostKeyChecking no\n\n" >> ~/.ssh/config
echo -e "    ConnectTimeout 5\n" >> ~/.ssh/config
echo -e "    ConnectionAttempts 20\n" >> ~/.ssh/config
echo -e "    ${nm}\n" >> ~/.ssh/config
echo -e "    ${user}\n" >> ~/.ssh/config

cat ~/.ssh/config




