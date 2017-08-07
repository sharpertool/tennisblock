# Introduction

I just use docker for a development postrgres, and development smtpd server.

# Installation

Install Docker for Mac, and make sure you have docker and docker-compose commands

# Docker Compose
The docker compose file dev.yml is used as the configuration.
To make this file the default, you need to set an environment variable in your shell.

    export COMPOSE_FILE=dev.yml

To make that easier, I have the godev script.. you have to source this, not run it.

    source godev

Or, you can use a dot

    . godev

