from bs4 import BeautifulSoup
import sys


kansou_titles = set()

# https://anidb.net/perl-bin/animedb.pl?web=1&unknown=1&tvspecial=1&tvseries=1&show=calendar&ova=1&other=1&musicvideo=1&movie=1&last.anime.year=2016&last.anime.month=16&h=0&do.last.anime=Show&do=calendar
#
# The relevant fields are 'last.anime.year', 'last.anime.month', and 'h' (they
# follow eachother consecutivally).
# 'last.anime.year': a year with format YYYY.
# 'last.anime.month': a month in the format 1M or M. If a 1 is prepended, then
#   M should be 3, 6, 9, or 12, representing the anime for Spring, Summer,
#   Fall, and Winter, respectively.  If a 1 is not prepended, then the results
#   show anime for that particular month only.
# 'h': 0, 1, or 2. This controls the mature content. 0 shows non-mature and
#   mature content.  1 shows only non-mature content, and 2 shows only mature
#   content.

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

def get_field(entry, name):
    try:
        return next((entry.find('div', class_=name).stripped_strings))
    except AttributeError:
        return ''

def get_anime(category='a'):
    if category == 'h':
        doc = BeautifulSoup(open('anidb_hentai.html'), 'lxml')
    else:
        doc = BeautifulSoup(open('anidb_season.html'), 'lxml')
    entries = doc.select('div.g_bubble.box')
    for entry in entries:
        name_en = get_field(entry, 'name')
        name_jp = get_field(entry, 'kanji')
        studio = get_field(entry, 'work')
        # Format is Dxx Month. D might need to have a zero prepended, and
        # Month needs to be converted to a number.
        date = get_field(entry, 'date')
        day = ''
        if (date[1].isdigit()):
            day = date[:2]
        else:
            day = '0' + date[0]
        month_beg = date.find(' ') + 1
        month = date[month_beg : ]
        new_date = '{y}-{m}-{d}'.format(y='2016', m=months_dict[month], d=day)
        type = get_field(entry, 'series')
        csv = 'null,{name},,,{date},{studio},,,'.format(name=name_en,
                                                        date=new_date,
                                                        studio=studio)
        if category == 'a':
            if name_jp in kansou_titles:
                print(csv)
            elif name_en in kansou_titles:
                print(csv)
            else:
                print('\nERROR: no match found.', name_en, name_jp, sep='\n')
                print('Enter "e" to use the English name, "s" to skip, or '+
                      'a different name:')
                name = input()
                if name == 'e':
                    name = name_en
                elif name == 's':
                    continue
                csv = 'null,{name},,,{date},{studio},,,'.format(name=name,
                                                                date=new_date,
                                                                studio=studio)
        # TODO: append to file.
        print(csv)

def get_anime_kansou():
    doc = BeautifulSoup(open('kansou_anime.html'), 'lxml')
    entries = doc.select('table.list tr')
    entry_iter = iter(entries)
    next(entry_iter) # Skip header row.
    for entry in entry_iter:
        try:
            first_td = entry.td
            second_td = first_td.next_sibling.next_sibling # Skip the newline.
            date = next(first_td.stripped_strings)
            date = date[: date.find('(')].replace('/', '-')
            name_jp = next(second_td.stripped_strings)
            kansou_titles.add(name_jp)
            #print(date, name_jp in kansou_titles)
        except AttributeError as err:
            # End of first table. Tables start with 'th' tags, so they can be
            # used as markers for the start of a new table. When a new table
            # starts, the try block tries to access 'td', but there are only
            # 'th', so an error is raised.
            print(str(err))
            break

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
        name_en = next(entry.find(class_='title-text').stripped_strings)
        studio = next(entry.find(class_='producer').stripped_strings)
        tot_eps = next(entry.find(class_='eps').stripped_strings)
        date = next(entry.find(class_='remain-time').stripped_strings)
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
        # TODO: escape "
        csv = '{name}}}}}{tot_eps}}}{date}}}{studio}}}}}}}\n'.\
                format(name=name_en,
                       tot_eps=tot_eps,
                       date=new_date,
                       studio=studio)
        csv_file_out.write(csv)
    # Print anything not found.
    for k in kansou_titles:
        if k not in entries:
            print(k)
    csv_file_out.close()

if len(sys.argv) < 4:
    print(
    """
    Usage: python anime_seasons.py <seasons> <beg_year> <end_year>

    Note: The arguments are space separated.  If a season appears twice, then
    the second is ignored.

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
