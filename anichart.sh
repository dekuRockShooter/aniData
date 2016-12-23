#!/bin/bash

YEAR_BEG=0
YEAR_END=0
GET_WINTER=0
GET_SPRING=0
GET_SUMMER=0
GET_FALL=0
HAS_SEASON_FLAG=0
ARG_WINTER=""
ARG_SUMMER=""
ARG_SPRING=""
ARG_FALL=""
ARG_WINTER_2=""
ARG_SUMMER_2=""
ARG_SPRING_2=""
ARG_FALL_2=""

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

while getopts "wfsp:b:e:h" opt;
do
    case $opt in
        w)
            GET_WINTER=1
            HAS_SEASON_FLAG=1
            WINTER_ARG="-w"
            WINTER_ARG_2="w"
            ;;
        p)
            GET_SPRING=1
            HAS_SEASON_FLAG=1
            SPRING_ARG="-p"
            SPRING_ARG_2="sp"
            ;;
        s)
            GET_SUMMER=1
            HAS_SEASON_FLAG=1
            SUMMER_ARG="-s"
            SUMMER_ARG_2="su"
            ;;
        f)
            GET_FALL=1
            HAS_SEASON_FLAG=1
            FALL_ARG="-f"
            FALL_ARG_2="f"
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

./get_seasons.sh $ARG_WINTER $ARG_SUMMER $ARG_FALL $ARG_SPRING -b $YEAR_BEG -e $YEAR_END
python anime_season.py $ARG_SUMMER_2 $ARG_SPRING_2 $ARG_WINTER_2 $ARG_FALL_2 $YEAR_BEG $YEAR_END
./import_csv_anime.sh -t a $ARG_WINTER $ARG_SUMMER $ARG_FALL $ARG_SPRING -b $YEAR_BEG -e $YEAR_END
./import_csv_anime.sh -t h $ARG_WINTER $ARG_SUMMER $ARG_FALL $ARG_SPRING -b $YEAR_BEG -e $YEAR_END
