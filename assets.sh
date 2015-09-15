#!/usr/bin/env bash

rm -rf static/collect/
if [ "$1" == "all" ]; then
    ./manage.py bower install
    ./manage.py bower freeze
fi
./manage.py collectstatic --noinput -i collect
./manage.py assets build