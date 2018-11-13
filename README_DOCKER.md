# Introduction

I just use docker for a development postrgres, and development smtpd server.

# Installation

Install Docker for Mac, and make sure you have docker and docker-compose commands

# Docker Compose
The docker compose file docker-compose.yml is used as the configuration.
This is the default compose file.
If you want to make your own copy,
then you can export the COMPOSE_FILE name to the custom name you used.

To make this file the default, you need to set an environment variable in your shell.

    export COMPOSE_FILE=my-docker-compose.yml

# Environment Setup

The compose file uses two environment variables

    SHARED_BACKUPS
    LOCAL_BACKUPS

Copy `example.env` to `.env` and update the values in that file to match your local system.

When you make changes to that file, you have to 're load' the container like this:

    docker-compose up -d

Then you can check the list-backups to see if your values work

    docker-compose exec postgres list-backups
    
# Start your containers!

Once you have source the godev script, or manually set DOCKER_COMPOSe environment variable, you can 
start your docker containers

	docker-compose up -d

The 'up' commands bring up the services in the compose file, and -d puts that into the background so your terminal
still works.

# Database Operations

You can list backups, backup and restore backups for your files.

Note, the default docker-compose.yml will put backups to:

	./DropboxTeam/database_backups

Please create a soft-link in your root project direct to point to the Docker location for the
Dropbox team.

    ln -s ~/Dropbox\ \(Sharpertool\)/ DropboxTeam

The link above will allow the docker-compose.yml to access this team folder, regadless of where it actually is, and also to avoid issues with the embedded spaces!

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
and if you have some other postgres tool, make sure it's not running either.







