#!/usr/bin/sh
./manage.py dumpdata --exclude user --exclude contenttypes --exclude auth.permission --exclude game --exclude sessions --exclude admin.logentry --indent 4 > initial.json