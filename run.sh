#!/bin/sh

set -e

make init test

# check log folder
LOG_DIR='./logs'
if [ ! -d "$LOG_DIR" ]; then
  echo "creating directory for logs ..."
  mkdir $LOG_DIR
fi

# check db folder
SQLITE_DIR='./data'
if [ ! -d "$SQLITE_DIR" ]; then
  echo "creating directory for data ..."
  mkdir $SQLITE_DIR
fi

python3 driver.py
