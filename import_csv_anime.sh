#!/bin/bash
#
# This script imports csv files created by anime_seasons.py into a database.
#
# Variables:
#   DB_NAME: the name of the database to import into
#   TYPE: either hentai or anime. If hentai, then the hentai csv files are
#         used. If anime, then the anime csv files are used.
#   YEAR_BEG: the year to start importing from.  csv files with a year in
#             [YEAR_BEG, YEAR_END] will be imported.
#             than or equal to this variable will be imported.
#   YEAR_END: the year to stop importing at.  csv files with a year in
#             [YEAR_BEG, YEAR_END] will be imported.

HENTAI_DB="Hentai.db"
ANIME_DB="Sybil.db"
DB_NAME="Hentai.db"
TYPE="hentai"
YEAR_BEG=1980
YEAR_END=2016
GET_WINTER=0
GET_SPRING=0
GET_SUMMER=0
GET_FALL=0
HAS_SEASON_FLAG=0

show_help() {
    echo 'This script imports csv files created by anime_seasons.py '\
         'into a database.'
    echo
    echo 'Flags'
    echo '-b n  the year to begin importing from. n should be a 4 digit year.'
    echo '-e n  the year to stop importing at. n should be a 4 digit year'
    echo '-w    import winter csv files.'
    echo '-p    import spring csv files.'
    echo '-s    import summer csv files.'
    echo '-f    import fall csv files.'
    echo '-t c  the type of csv to import. The argument, c, should be a or h.'\
         '      If h, then the hentai csv files are used. If a, then the '\
         '      anime csv files are used.'
    echo '-h    show this help message.'
}

YEAR_REGEX="[0-9]{4}"

while getopts "wfspt:b:e:h" opt;
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
        t)
            if [ "$OPTARG" == "a" ];
            then
                TYPE="anime"
                DB_NAME="$ANIME_DB"
            elif [ "$OPTARG" == "h" ];
            then
                TYPE="hentai"
                DB_NAME="$HENTAI_DB"
            else
                echo "-t argument must be a or h"
                exit
            fi
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
            exit
            ;;
    esac
done

if [ "$HAS_SEASON_FLAG" == 0 ];
then
    echo "Seasons not specified."\
         "At least one of -w, -p, -s, and -f must be given."
    exit
fi

sqlite3 $DB_NAME "CREATE TABLE 'Temp' (Name varchar(30), 'Episodes Watched' unsigned smallint, 'Total Episodes' unsigned SmallInt, 'Date Aired' Date, 'Production Studio' varchar(30), Score unsigned Double(3,2), Genres varchar(100), Notes varchar(256));"
for year in $(seq $YEAR_BEG $YEAR_END);
do
    if [ "$GET_WINTER" == 1 ];
    then
        sqlite3 $DB_NAME '.separator }' ".import w"$year"_"$TYPE".csv Temp"
    fi
    if [ "$GET_SPRING" == 1 ];
    then
        sqlite3 $DB_NAME '.separator }' ".import sp"$year"_"$TYPE".csv Temp"
    fi
    if [ "$GET_SUMMER" == 1 ];
    then
        sqlite3 $DB_NAME '.separator }' ".import su"$year"_"$TYPE".csv Temp"
    fi
    if [ "$GET_FALL" == 1 ];
    then
        sqlite3 $DB_NAME '.separator }' ".import f"$year"_"$TYPE".csv Temp"
    fi
done
sqlite3 $DB_NAME "insert into Main ('Name', 'Episodes Watched', 'Total Episodes', 'Date Aired', 'Production Studio', 'Score', 'Genres', 'Notes') select * from Temp;"
sqlite3 $DB_NAME 'DROP TABLE Temp;'
