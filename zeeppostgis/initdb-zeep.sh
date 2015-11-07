#!/bin/sh

SQLDIR="/zeep/zeeppostgis"

su - postgres -c "createdb -T template_postgis zeepdata"

