#!/bin/bash
# some pre-start operation

nginx

LOGGING_OPTIONS=""
re='^[0-9]+$'
if [[ ${EODAG_LOGGING} =~ $re ]] && [ "${EODAG_LOGGING} " -gt "0" ]; then
   LOGGING_OPTIONS="-"$(printf '%0.sv' $(seq 1 ${EODAG_LOGGING}))
else
    echo "Logging level can be changed using EODAG_LOGGING environment variable [1-3]"
fi

#export EODAG_CORS_ALLOWED_ORIGINS=http://127.0.0.1:5001

# start
exec "$@" &
exec eodag $LOGGING_OPTIONS serve-rest -w
