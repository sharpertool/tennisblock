# Introduction

This is my tennisblock.com site.

# Setting up

There are two directories I'll talk about. GIT_ROOT, and DJANGO_ROOT, or GR, and DR, for short.

GR is the base of the repo, DR is tennisblock.. just so you know.


## Local Config Files

In GR, you need to copy .env.example to .env.
This file is used by docker, so the values in there configure the docker system.

In DJANGO_ROOT, there are two local files that are used configurable.

Copy .env.local.example to .env.loocal

	cd tennisblock
	cp .env.local.example .env.local

Edit the values as appropriate

Finally, get the local config

	cd tennisblock
	cp local_config.sample.py local_config.py

Edit




