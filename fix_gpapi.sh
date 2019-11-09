#!/bin/bash

GPAPI_LOCATION=$(pip show gpapi | grep Location | awk '{print $2}' )

CONF_LOCATION="$GPAPI_LOCATION/gpapi/conf.py"

sed -i '143d' $CONF_LOCATION
