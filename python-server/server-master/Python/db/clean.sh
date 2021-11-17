#!/bin/sh

CURRENT_DIR=`dirname $0`

HOST="127.0.0.1"
DATABASE="dyscalculia"
USER="root"

echo "Cleaning database"

mysql -u${USER} -h${HOST} -e "SET SESSION sql_mode = 'STRICT_ALL_TABLES'; source $CURRENT_DIR/script/clean.sql ;" ${DATABASE}
