#! /bin/bash

#####
# Postgres: wait until container is created
#
# $?                most recent foreground pipeline exit status
# > /dev/null 2>&1  get stderr while discarding stdout
####
python /zeep/database-check.py > /dev/null 2>&1
while [[ $? != 0 ]] ; do
    sleep 1; echo "*** Waiting for postgres container ..."
    python /zeep/database-check.py > /dev/null 2>&1
done

#####
# Django setup
#####
service ssh restart
python /zeep/manage.py migrate
hx start --dev --settings zeep.settings
#python /zeep/manage.py runserver 0.0.0.0:8000