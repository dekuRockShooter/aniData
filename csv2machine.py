import sys


def convert(season, year, csv_out, header=True):
    csv_in= open(season + year + '_anime.csv', 'r')
    genre_map = {
        "Action": 0,
        "Adventure": 1,
        "Cars": 2,
        "Comedy": 3,
        "Dementia": 4,
        "Demons": 5,
        "Drama": 6,
        "Ecchi": 7,
        "Fantasy": 8,
        "Game": 9,
        "Harem": 10,
        "Historical": 11,
        "Horror": 12,
        "Josei": 13,
        "Magic": 14,
        "Martial Arts": 15,
        "Mecha": 16,
        "Military": 17,
        "Music": 18,
        "Mystery": 19,
        "Parody": 20,
        "Police": 21,
        "Psychological": 22,
        "Romance": 23,
        "Samurai": 24,
        "School": 25,
        "Sci-Fi": 26,
        "Seinen": 27,
        "Shoujo": 28,
        "Shoujo Ai": 29,
        "Shounen": 30,
        "Shounen Ai": 31,
        "Slice of Life": 32,
        "Space": 33,
        "Sports": 34,
        "Super Power": 35,
        "Supernatural": 36,
        "Thriller": 37,
        "Vampire": 38,
    }

    csv = '{f3},{f4_1},{f4_2},{f4_3},{f5},{f7},{f8},{f9},{f10}'\
            .format(f3='tot_eps',
                    f4_1='year',
                    f4_2='month',
                    f4_3='day',
                    f5='studio',
                    f7=','.join(genre_map.keys()),
                    f8='tot_watched',
                    f9='score',
                    f10='source',
                    )
    #print(csv)
    if header:
        csv_out.write(csv + '\n')

    # Occultic;Nine}}?}2016-10-08}A-1 Pictures}}Mystery,Sci-Fi}
    # f1}f2}f3}f4}f5}f6}f7}f8
    for line in csv_in:
        #csv = name}}eps_watch}}eps_tot}}date_air}}studio}}score}}genre}}notes
        fields = line.strip().split('}')
        bool_vec = ["N" for _ in range(0, len(genre_map))]
        for genre in fields[6].split(','):
            try:
                bool_vec[genre_map[genre]] = "Y"
            except KeyError:
                print("****Warning: Skipping unmapped genre ", genre)
                continue
        date = fields[3].split('-')
        csv = '{f3},{f4_1},{f4_2},{f4_3},{f5},{f7},{f8},{f9},{f10}'\
            .format(
                    f3=fields[2],
                    f4_1=date[0],
                    f4_2=date[1],
                    f4_3=date[2],
                    f5=fields[4],
                    f7=','.join(bool_vec),
                    f8=fields[7],
                    f9=fields[8],
                    f10=fields[9],
                   )
        #print(csv)
        csv_out.write(csv + '\n')

    csv_in.close()

if len(sys.argv) < 4:
    print(
    """
    Usage: python anime_seasons.py <seasons> <beg_year> <end_year>

    <seasons>
    At least one of w, f, sp, and su.

    <beg_year>
    The first year to get charts from (four digits).

    <beg_year>
    The last year to get charts from (four digits).

    """
    )
    exit()

beg_year = int(sys.argv[-2])
end_year = int(sys.argv[-1])
assert beg_year <= end_year
assert ((beg_year / 1000) > 1) and ((beg_year / 1000) < 10)
assert ((end_year / 1000) > 1) and ((end_year / 1000) < 10)
assert len(sys.argv) < 8
seasons = set()
for season in sys.argv[1:-2]:
    if season not in ('sp', 'su', 'f', 'w'):
        print("Invalid season:", season, "See help for valid seasons.")
        exit()
    seasons.add(season)
assert (len(seasons) > 0) and (len(seasons) < 5)
csv_out= open('anime_mach.csv', 'a')
header = True
for season in seasons:
    for year in range(beg_year, end_year + 1):
        if header:
            convert(season, str(year), csv_out, True)
            header = False
        else:
            convert(season, str(year), csv_out, False)
csv_out.close()
