#!/bin/bash

http_proxy='173.201.183.172:8000'

for year in $(seq 2013 2015);
do
    http_proxy='173.201.183.172:8000'
    #wget myanimelist.net/anime/season/$year/spring -O sp$year.html
    http_proxy='201.55.46.6:80'
    wget myanimelist.net/anime/season/$year/fall -O f$year.html
    sleep 90
done
