csv_in= open('f2016_anime.csv', 'r')
machine_out= open('f2016_anime_mach.csv', 'w')
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
print(csv)

# Occultic;Nine}}?}2016-10-08}A-1 Pictures}}Mystery,Sci-Fi}
# f1}f2}f3}f4}f5}f6}f7}f8
for line in csv_in:
    #csv = name}}eps_watch}}eps_tot}}date_air}}studio}}score}}genre}}notes
    fields = line.split('}')
    bool_vec = ["0" for _ in range(0, len(genre_map))]
    for genre in fields[6].split(','):
        try:
            bool_vec[genre_map[genre]] = "1"
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
    print(csv)


