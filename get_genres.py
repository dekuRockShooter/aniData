# A quick beautifulsoup4 primer
#
# Initialization:
# doc = BeautifulSoup(open('anidb_hentai.html'), 'lxml')
#
# Searching for elements:
# doc.find_all('div', class_='r18') # Get all <div class="r18">
# genre_ids = doc.find(id='genres') # Find tag by id.
# entries = doc.find_all(is_not_hentai) # Find tags that make predicate true.
#
# Getting attributes values and text.
# id = genre_id.get('id') # Get the value of the id attribute.
# elem['class'] # Get the value class of the class attribute.
# genre  = genre_id.get_text() # Get the text node of an element.
# tag.has_attr('class')
from bs4 import BeautifulSoup
import sys


genre_map = {}
kansou_titles = set()

months_dict = {
        'January': '01',
        'February': '02',
        'March': '03',
        'April': '04',
        'May': '05',
        'June': '06',
        'July': '07',
        'August': '08',
        'September': '09',
        'October': '10',
        'November': '11',
        'December': '12',
        'Jan': '01',
        'Feb': '02',
        'Mar': '03',
        'Apr': '04',
        'May': '05',
        'Jun': '06',
        'Jul': '07',
        'Aug': '08',
        'Sep': '09',
        'Oct': '10',
        'Nov': '11',
        'Dec': '12'
        }


def get_mal_season(season, year, category='a'):
    """Extract data from a MAL season web page into a csv file.

    This function gets the name, total episodes, date aired, and
    production studio from an html page of the webpage of the form:

        http://myanimelist.net/anime/season/<year>/<season>

    where <year> is a four digit year (2000, 2009, etc.) and <season>
    is one of: winter, spring, summer, fall.  The html file must be
    named <season><year>.html, where <year> is a four digit year, and
    <season> is one of: w, sp, su, f.  Note, this does not download
    the web page.  It is assumed to already exist in the file system.

    The data is written to a csv file named <season><year>_<type>.csv,
    where <season> is one of: w, sp, su, f; <year> is a four digit
    year; and <type> is either anime or hentai.

    The csv file has eight fields separated by a } character.  The
    meaning of each field is:

        field 1: name of the anime
        field 2: empty
        field 3: number of episodes
        field 4: date aired as YYYY-MM-DD
        field 5: animation studio
        field 6: empty
        field 7: empty
        field 8: empty

    This file is meant to be easily imported into a table that has the
    same schema as the tables in the Sybil database.

    Args:
        season (str): one of w, sp, su, and f as part of the name of
                      the html file to extract data from.
        year (str): A four digit string representing a year. This is
                    part of the name of the html file to extract data
                    from.
        category (char): one of a and h.  If a, then data for
                         non-hentai shows is extracted.  If h, then
                         data for hentai only is extracted.
    """
    csv_filename = ''
    csv_file_out = None
    html_filename = season + year + '.html'
    doc = BeautifulSoup(open(html_filename), 'lxml')
    entries = []
    # The index at which the day field starts in the extracted date.
    day_beg_idx = 4 
    genre_ids = doc.find(id='genres')
    for genre_id in genre_ids.find_all('li'):
        id = genre_id.get('id')
        genre = genre_id.find(id=id)
        genre_map[id] = genre_id.get_text()
    if category == 'a':
        csv_filename = season + year + '_anime.csv'

        def is_not_hentai(tag):
            """Check if a tag represents a non-hentai entry or not."""
            # Non-hentai entries can be identified in two ways.  They can have
            # two classes, one of them being seasonal-anime.  Or they can have
            # a class called kids.
            if tag.has_attr('class'):
                class_attr = tag['class']
                if (len(class_attr) == 2 and\
                    'seasonal-anime' in class_attr) or\
                    'kids' in class_attr:
                    return True
            return False

        entries = doc.find_all(is_not_hentai)
    elif category == 'h':
        csv_filename = season + year + '_hentai.csv'
        # hentai entries can be identified as those having a class of r18.
        entries = doc.find_all('div', class_='r18')
    csv_file_out = open(csv_filename, 'w')
    # Extract data.
    # The name is the text of the tag with class title-text.
    # The animation studio is the text of the tag with class producer.
    # The number of episodes is the text of the tag with class eps.
    # The date aired is the text of the tag with class remain-time.
    for entry in entries:
        genres = entry.get('data-genre').split(',')
        genre_names = []
        for genre_id in genres:
            try:
                genre_names.append(genre_map[genre_id])
            except KeyError:
                pass
        name_en = next(entry.find(class_='title-text').stripped_strings)
        studio = next(entry.find(class_='producer').stripped_strings)
        tot_eps = next(entry.find(class_='eps').stripped_strings)
        source = next(entry.find(class_='source').stripped_strings)
        tot_watched = next(entry.find(class_='member fl-r').stripped_strings)
        score = next(entry.find(class_='score').stripped_strings)
        date = next(entry.find(class_='remain-time').stripped_strings)
        type  = entry.find(class_="info").get_text().lstrip()
        type = type[: type.find(' ')]
        # tot_eps has form '#eps eps'. Get only #eps.
        sep_idx = tot_eps.find(' ')
        if sep_idx != -1:
            tot_eps = tot_eps[: sep_idx]
        # 'date' has form MMM D, YYYY, time.  This gets only the date.
        sep_idx = date.find(',', 10)
        if sep_idx != -1:
            date = date[: sep_idx]
        month = months_dict[date[: 3]]
        day = date[day_beg_idx]
        if date[day_beg_idx + 1].isdigit():
            day = day + date[day_beg_idx + 1]
        else:
            day = '0' + day
        year = date[-4 :]
        new_date = '{y}-{m}-{d}'.format(y=year, m=month, d=day)
        #csv = name}}eps_watch}}eps_tot}}date_air}}studio}}score}}genre}}notes
        csv = '{name}}}}}{tot_eps}}}{date}}}{studio}}}}}{genres}}}{tot_watch}}}{score}}}{source}}}{type}\n'.\
                format(name=name_en.replace("\"", "\\\""),
                       tot_eps=tot_eps,
                       date=new_date,
                       studio=studio,
                       genres=','.join(genre_names),
                       tot_watch=tot_watched.replace(',', ''),
                       score=score,
                       source=source,
                       type=type
                      )
        csv_file_out.write(csv)
    # Print anything not found.
    for k in kansou_titles:
        if k not in entries:
            print(k)
    csv_file_out.close()

if len(sys.argv) < 4:
    print(
    """
    This program creates csv files that contain the name, total episodes, date
    aired, and production studio of an anime by extracting the data from an
    html file from the URL:

        http://myanimelist.net/anime/season/<year>/<season>

    where <year> is a four digit year (2000, 2009, etc.) and <season>
    is one of winter, spring, summer, fall.  It does not download the page,
    but assumes that a copy exists locally and is named <season><year>.html,
    where <year> is a four digit year, and <season> is one of w, sp, su, f.

    The generated csv files are named <season><year>_anime.csv and
    <season><year>_hentai.csv, where <season> and <year> are the same as
    above.

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
for season in seasons:
    for year in range(beg_year, end_year + 1):
        get_mal_season(season, str(year), 'a')
        get_mal_season(season, str(year), 'h')
#get_anime_kansou()
#get_mal_season('f', str(2016))
#get_mal_season('f', str(2016), 'h')
