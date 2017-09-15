#!/bin/sh

NOW=$(date +"%F-%H%M")
LOG='blitz_'$NOW'.log'
ERRLOG='error_'$NOW'.log'

LOG_FOLDER='./logs'

# python3 driver.py 2> $LOG_FOLDER/$ERRLOG 1> $LOG_FOLDER/$LOG
# python3 driver.py > $LOG_FOLDER/$LOG 2>&1
python3 driver.py

