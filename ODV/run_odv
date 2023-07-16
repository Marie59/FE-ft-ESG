#!/bin/sh -f

# script to run Ocean Data View 64 bit on a Linux 64 bit system

# edit the lines immediately following #TODO, set execute attribute and
# move to a directory in your path. USAGE: run_odv [collection]

# © 2023 Reiner Schlitzer,
#        Alfred Wegener Institute,
#        Bremerhaven, Germany
#        Reiner.Schlitzer@awi.de


#TODO: set ODVHOME to the full path-name of the odv install-directory
ODVHOME=/app/odv


#-----------------------------------------------------------------------
# nothing to be changed below this line

# set LD_LIBRARY_PATH
if [ -z LD_LIBRARY_PATH ]
then
LD_LIBRARY_PATH=${ODVHOME}/bin_linux-amd64
else
LD_LIBRARY_PATH=${ODVHOME}/bin_linux-amd64:${LD_LIBRARY_PATH}
fi

# set PATH
PATH=${PATH}:${ODVHOME}/bin_linux-amd64

export LD_LIBRARY_PATH
export PATH

exec ${ODVHOME}/bin_linux-amd64/odv $1 $2 $3 $4 $5
