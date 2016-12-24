#!/bin/bash
#
#

YEAR_BEG=1980
YEAR_END=2016
GET_WINTER=0
GET_SPRING=0
GET_SUMMER=0
GET_FALL=0
HAS_SEASON_FLAG=0

if [ "$#" == 0 ];
then
    echo -e "\n"\
         "This program downloads the anime chart for given seasons and years\n"\
         "from myanimelist.net.  So as to not overload MAL's servers, there\n"\
         "is a 30 second pause between downloads.  The charts are saved as\n"\
         "<season><year>.html, where <season> is w, sp, su, or f, depending\n"\
         "on the arguments given, and <year> is any year between (inclusive)\n"\
         "the years given in the arguments."

    echo -e "\n\nUsage:\n"\
         "    ./get_seasons.sh <seasons> <years>\n"\
         "Both year arguments, and at least one season argument must be given."

    echo -e "\n\n<seasons>\n"\
         "-w    Download the winter anime page\n"\
         "-p    Download the spring anime page\n"\
         "-s    Download the summer anime page\n"\
         "-f    Download the fall anime page"\
         "\n\n<years>\n"\
         "-b n  A four digit year, marking the first year to get charts from\n"\
         "-e n  A four digit year, marking the last year to get charts to"\
         "\n\nOther:\n"\
         "-h    Show this message\n"

    echo -e "\n\nExample\n"\
         "Download the charts for winter and fall anime for the years 2010 to"\
         "2016:\n\n"\
         "    $ ./get_seasons.sh -w -f -b 2010 -e 2016\n\n"\
         "The charts are saved in w2010.html, f2010.html, ..., w2016.htm,"\
         "f2016.html.\n"
    exit
fi

while getopts "wfspb:e:h" opt;
do
    case $opt in
        w)
            GET_WINTER=1
            HAS_SEASON_FLAG=1
            ;;
        p)
            GET_SPRING=1
            HAS_SEASON_FLAG=1
            ;;
        s)
            GET_SUMMER=1
            HAS_SEASON_FLAG=1
            ;;
        f)
            GET_FALL=1
            HAS_SEASON_FLAG=1
            ;;
            #TODO check if it's less than YEAR_END
        b)
            if [[ $OPTARG =~ $YEAR_REGEX ]];
            then
                YEAR_BEG=$OPTARG
            else
                echo "-b argument must be a 4-digit integer"
                exit
            fi
            ;;
        e)
            if [[ $OPTARG =~ $YEAR_REGEX ]];
            then
                YEAR_END=$OPTARG
            else
                echo "-b argument must be a 4-digit integer"
                exit
            fi
            ;;
        h)
            show_help
            ;;
    esac
done

if [ "$HAS_SEASON_FLAG" == 0 ];
then
    echo "Seasons not specified."\
         "At least one of -w, -p, -s, and -f must be given."
    exit
fi

http_proxy='173.201.183.172:8000'

#for year in $(seq 2013 2015);
#do
    #http_proxy='173.201.183.172:8000'
    ##wget myanimelist.net/anime/season/$year/spring -O sp$year.html
    #http_proxy='201.55.46.6:80'
    #wget myanimelist.net/anime/season/$year/fall -O f$year.html
    #sleep 90
#done

for year in $(seq $YEAR_BEG $YEAR_END);
do
    if [ "$GET_WINTER" == 1 ];
    then
        wget myanimelist.net/anime/season/$year/winter -O w$year.html
        sleep 30
    fi
    if [ "$GET_SPRING" == 1 ];
    then
        wget myanimelist.net/anime/season/$year/spring -O sp$year.html
        sleep 30
    fi
    if [ "$GET_SUMMER" == 1 ];
    then
        wget myanimelist.net/anime/season/$year/summer -O su$year.html
        sleep 30
    fi
    if [ "$GET_FALL" == 1 ];
    then
        wget myanimelist.net/anime/season/$year/fall -O f$year.html
        sleep 30
    fi
done
