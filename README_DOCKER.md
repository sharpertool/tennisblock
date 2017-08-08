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

# Start your containers!

Once you have source the godev script, or manually set DOCKER_COMPOSe environment variable, you can 
start your docker containers

	docker-compose up -d

The 'up' commands bring up the services in the compose file, and -d puts that into the background so your terminal
still works.

# Database Operations

You can list backups, backup and restore backups for your files.

Note, the default dev.yml will put backups to:

	~/Dropbox/Development/tennisblock/backups

This directory kind of needs to exist.. But, you can change dev.yml to have whatever path you want. Don't commit
this.. it's okay if it's different... you can also make a copy fo that and change godev to use your copy.

For all of the operations, we use docker-compose, and we exec an operation on the service. The services are named:
	
	postgres
	smtpd

## List Backups

	docker-compose exec postgres list-backups

## Backup your DB

	docker-compose exec postgres backup


## Restore a backup

List backups, and then use just the filename part for the filename in the following command:

	docker-compose exec postgres restore <filename>

NOTE: If you have some tool using the DB, restore won't work. This is a postgres thing.. make sure Django isn't running,
and if you have some postgres tool, make sure it's not running either.







