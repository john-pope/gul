#!/bin/bash

source $HOME/.profile

args=()

args+=( 'uvicorn' )
args+=( 'main:app' )
args+=( '--host' )
args+=( '0.0.0.0' )
args+=( '--port' )
args+=( 8080 )

if [ "$ENVIRONMENT" != "production" ]; then
    args+=( '--reload' )
    args+=( '--ssl-certfile' )
    args+=( '/ssl/self-signed-cert' )

    echo "Running in development mode"
    echo "ARGS=${args[@]}"
    echo ""
    echo "Start app with:"
    echo ""
    echo "/app/docker/run-app"
    echo ""
fi

export ARGS="${args[@]}"

if [ "$1" != 'bash' ]; then
    /bin/bash $@
else
    $@
fi