# Introduction

This is my tennisblock.com site.

# Setting up

There are two directories I'll talk about. GIT_ROOT, and DJANGO_ROOT, or GR, and DR, for short.

GR is the base of the repo, DR is tennisblock.. just so you know.

# Python Setup

This project works on Python 2.7.x.. latest is better.

Create a new local virtualenv

	virtualenv .venv

Activate your virtualenv

	source .venv/bin/activate

Install requirements -- these are for development

	pip install -r requirements/test.txt

## Local Config Files

In GR, you need to copy .env.example to .env.
This file is used by docker, so the values in there configure the docker system.

In DJANGO_ROOT, there are two local files that are used for configuration.

Copy .env.local.example to .env.local

	cd tennisblock
	cp .env.local.example .env.local

Edit the values as appropriate

Finally, get the local config

	cd tennisblock
	cp local_config.sample.py local_config.py

You will need to edit this file to customize it to your local environment. Collaborate with team leader or other members of the team to get the right values, as the example might not be up-to-date






