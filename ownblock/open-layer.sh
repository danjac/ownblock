#! /usr/bin/env bash

cd static/bower_components/openlayers/build

./build.py

if [ ! -h "img" ]
then
    ln -s ../img .
fi

if [ ! -h "theme" ]
then
    ln -s ../theme .
fi

cd ../../../..
