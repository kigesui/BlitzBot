#!/bin/sh

# NOW=$(date +"%F-%H%M")
# LOG='blitz_'$NOW'.log'
# ERRLOG='error_'$NOW'.log'

# check log folder
LOG_DIR='./logs'
if [ ! -d "$LOG_DIR" ]; then
  echo "creating directory for logs ..."
  mkdir $LOG_DIR
fi

# check db folder
SQLITE_DIR='./data'
if [ ! -d "$SQLITE_DIR" ]; then
  echo "creating directory for directory ..."
  mkdir $SQLITE_DIR
fi


python3 driver.py
