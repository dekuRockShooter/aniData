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
         "This program downloads anime data for given seasons of a given\n"\
         "range of years and inserts them into a database.  It is equivalent"\
         "\nto this sequence of calls:\n\n"\
         "    $ ./get_seasons.sh <args>\n"\
         "    $ ./import_csv_anime.sh <args> -t a\n"\
         "    $ ./import_csv_anime.sh <args> -t h\n\n"\
         "where <args> are the arguments to each program that are\n"\
         "appropriately formatted from the arguments given to anichart.sh.\n"\
         "\nThe databases into which data are inserted are Sybil.db and\n"\
         "Hentai.db, both of which must exist in the working directory and\n"\
         "have a schema usable by aniLog.py."
    echo -e "Usage:\n"\
         "    $ ./anichart.sh <seasons> <years>\n"\
         "Both year arguments, and at least one season argument must be given."

    echo -e "\n\n<seasons>\n"\
         "-w    Get winter anime data\n"\
         "-p    Get spring anime data\n"\
         "-s    Get summer anime data\n"\
         "-f    Get fall anime data"\
         "\n\n<years>\n"\
         "-b n  A four digit year, marking the first year to get data from\n"\
         "-e n  A four digit year, marking the last year to get data to"\
         "\n\nOther:\n"\
         "-h    Show this message\n"
    exit
fi

while getopts "wfspb:e:h" opt;
do
    case $opt in
        w)
            GET_WINTER=1
            HAS_SEASON_FLAG=1
            ARG_WINTER="-w"
            ARG_WINTER_2="w"
            ;;
        p)
            GET_SPRING=1
            HAS_SEASON_FLAG=1
            ARG_SPRING="-p"
            ARG_SPRING_2="sp"
            ;;
        s)
            GET_SUMMER=1
            HAS_SEASON_FLAG=1
            ARG_SUMMER="-s"
            ARG_SUMMER_2="su"
            ;;
        f)
            GET_FALL=1
            HAS_SEASON_FLAG=1
            ARG_FALL="-f"
            ARG_FALL_2="f"
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
    echo "Run with no arguments for help."
    exit
fi

./get_seasons.sh $ARG_WINTER $ARG_SUMMER $ARG_FALL $ARG_SPRING -b $YEAR_BEG -e $YEAR_END
python anime_season.py $ARG_SUMMER_2 $ARG_SPRING_2 $ARG_WINTER_2 $ARG_FALL_2 $YEAR_BEG $YEAR_END
./import_csv_anime.sh -t a $ARG_WINTER $ARG_SUMMER $ARG_FALL $ARG_SPRING -b $YEAR_BEG -e $YEAR_END
./import_csv_anime.sh -t h $ARG_WINTER $ARG_SUMMER $ARG_FALL $ARG_SPRING -b $YEAR_BEG -e $YEAR_END
