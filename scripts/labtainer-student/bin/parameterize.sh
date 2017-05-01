#!/usr/bin/env bash
: <<'END'
This software was created by United States Government employees at 
The Center for the Information Systems Studies and Research (CISR) 
at the Naval Postgraduate School NPS.  Please note that within the 
United States, copyright protection is not available for any works 
created  by United States Government employees, pursuant to Title 17 
United States Code Section 105.   This software is in the public 
domain and is not subject to copyright. 
END
# parameterize.sh
#
# Usage: parameterize.sh <LAB_INSTANCE_SEED>
# Arguments:
#     <LAB_INSTANCE_SEED> -- laboratory instance seed
# 
# Description:
# 1. Call ParameterParser.py (passing $LAB_INSTANCE_SEED)
# 2. If file .local/bin/fixlocal.sh exist, run it

#echo "Parameterizing laboratory"

# Configuration variables
LAB_SEEDFILE="/home/ubuntu/.local/.seed"
USER_EMAILFILE="/home/ubuntu/.local/.email"
LAB_NAMEFILE="/home/ubuntu/.local/.labname"
LAB_PARAMCONFIGFILE="/home/ubuntu/.local/config/parameter.config"

# Do not display instruction during parameterization
LOCKDIR=/tmp/.mylockdir
mkdir "$LOCKDIR" >/dev/null 2>&1

#echo "number of argument is $#"
#echo "argument is $@"

if [ $# -ne 4 ]
then
    echo "Usage: parameterize.sh <LAB_INSTANCE_SEED> <USER_EMAIL> <LAB_NAME> <CONTAINER_NAME>"
    echo "       <LAB_INSTANCE_SEED> -- laboratory instance seed"
    echo "       <USER_EMAIL> -- user's e-mail"
    echo "       <LAB_NAME> -- name of the lab"
    echo "       <CONTAINER_NAME> -- name of the container"
    exit 1
fi

LAB_INSTANCE_SEED=$1
USER_EMAIL=$2
LAB_NAME=$3
CONTAINER_NAME=$4

# Laboratory instance seed is always stored in $LAB_SEEDFILE
echo "$LAB_INSTANCE_SEED" > $LAB_SEEDFILE
# User's e-mail is always stored in $USER_EMAILFILE
echo "$USER_EMAIL" > $USER_EMAILFILE
echo "$LAB_NAME" > $LAB_NAMEFILE

# call ParameterParser.py (passing $LAB_INSTANCE_SEED)
sudo /home/ubuntu/.local/bin/ParameterParser.py $LAB_INSTANCE_SEED $CONTAINER_NAME $LAB_PARAMCONFIGFILE

# If file /home/ubuntu/.local/bin/fixlocal.sh exist, run it
if [ -f /home/ubuntu/.local/bin/fixlocal.sh ]
then
    /home/ubuntu/.local/bin/fixlocal.sh 2>>/tmp/fixlocal.output
fi

rmdir $LOCKDIR
