#!/bin/bash

TIKA_PORT=9998
TIKA_HOST=localhost
CURRENT_USER=$(whoami) 
TIKA_JAR_URL="http://search.maven.org/remotecontent?filepath=org/apache/tika/tika-server/1.24/tika-server-1.24.jar"
TIKA_WORKSPACE=$HOME/lib
TIKA_FILE_NAME="tika_server.jar"

echo -e "Current user: $CURRENT_USER"

if [ ! -f $TIKA_WORKSPACE/$TIKA_FILE_NAME ]; then
    echo -e "Downloading tika-server.jar"

    if [ ! -d "$TIKA_WORKSPACE" ]; then
        echo -e "making tika workspace"
        mkdir $TIKA_WORKSPACE
    fi

    wget -c $TIKA_JAR_URL -O $TIKA_WORKSPACE/$TIKA_FILE_NAME 
fi

echo -e "## Setting environment vars"

export TIKA_SERVER_ENDPOINT="http://$TIKA_HOST:$TIKA_PORT"
echo -e "TIKA_SERVER_ENDPOINT to $TIKA_SERVER_ENDPOINT"

export TIKA_CLIENT_ONLY=True
echo -e "TIKA_CLIENT_ONLY to $TIKA_CLIENT_ONLY"

echo -e "## Starting tika server on: $TIKA_WORKSPACE"
cd $TIKA_WORKSPACE

java -jar tika_server.jar -h $TIKA_HOST