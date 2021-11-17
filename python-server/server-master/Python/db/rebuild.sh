#!/bin/sh

CURRENT_DIR=`dirname $0`

HOST="127.0.0.1"
DATABASE="dyscalculia"
USER="root"

echo "Building Database: $DATABASE on $HOST"

## 1) Delete any existing database

echo "Deleting existing database:"

mysql -u ${USER} -h ${HOST} -e "drop database if exists $DATABASE;"

if [ $? -ne 0 ]; then
    echo "WARNING: last command returned $?"
    exit 1
fi

## 2) Create a new database

echo "Creating new database:"

mysql -u${USER} -h${HOST} -e "create database $DATABASE;"

if [ $? -ne 0 ]; then
    echo "WARNING: last command returned $?"
    exit 1
fi

## 3) Create the empty schema

echo "Creating empty schema:"

mysql -u${USER} -h${HOST} -e "SET SESSION sql_mode = 'STRICT_ALL_TABLES'; source $CURRENT_DIR/script/schema.sql ;" ${DATABASE}

if [ $? -ne 0 ]; then
    echo "WARNING: last command returned $?"
    exit 1
fi
