import django, os
import spartigamisite.settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spartigamisite.settings')
django.setup()

from spartigamiapp.models import Game, ScorePair, TableData

games = Game.objects.all()
pairs = ScorePair.objects.all()
max_games = ScorePair.objects.order_by('-games')[0].games

EXCLUDE_LIST = [1, 2, 4, 7, 11, 16, 29]
COLS = 104
ROWS = 50

count_stats = list()
count_color = list()
record_stats = list()
record_color = list()
season_stats = list()
season_color = list()
latest_stats = list()
latest_color = list()


def calc_count_color(games, max_games):
    scalar = (max_games - games) / max_games
    scalar = scalar ** 3
    r = 0 + 192 * scalar
    g = 128 + 96 * scalar

    return f'rgb({r}, {g}, {r})'


def calc_record_color(pct):
    r = min(256 * (1 - pct), 128)
    g = min(256 * pct, 128)

    return f'rgb({r}, {g}, 0)'


def calc_season_color(season):
    scalar = (2023 - season) / 105
    scalar = scalar ** (1 / 3)
    r = 0 + 192 * scalar
    g = 128 + 96 * scalar

    return f'rgb({r}, {g}, {r})'


for c in range(COLS + 1):
    for r in range(c + 1):
        index = r + c * (c + 1) // 2
        try:
            entry = pairs.get(high = c, low = r)

            count_stats.append(entry.games)
            count_color.append(calc_count_color(entry.games, max_games))

            w, l, t = entry.record.split('-')
            pct = (int(w) + 0.5 * float(t)) / (int(w) + int(l) + int(t))
            record_stats.append('%0.3f' % pct)
            record_color.append(calc_record_color(pct))

            game = games.get(date = entry.first_game)
            season_stats.append(game.season)
            season_color.append(calc_season_color(int(game.season)))

            game = games.get(date = entry.last_game)
            latest_stats.append(game.season)
            latest_color.append(calc_season_color(int(game.season)))

        except:
            count_stats.append(0)
            record_stats.append(0)
            season_stats.append(0)
            latest_stats.append(0)
            
            if index not in EXCLUDE_LIST:
                count_color.append('rgb(255, 255, 255)')
                record_color.append('rgb(255, 255, 255)')
                season_color.append('rgb(255, 255, 255)')
                latest_color.append('rgb(255, 255, 255)')

            else:
                count_color.append('rgb(0, 0, 0)')
                record_color.append('rgb(0, 0, 0)')
                season_color.append('rgb(0, 0, 0)')
                latest_color.append('rgb(0, 0, 0)')

print('uploading...')
table_data = TableData.objects.all()
for i in range(len(count_stats)):
    if table_data.filter(index = i).exists():
        instance = table_data.get(index = i)
        instance.games = count_stats[i]
        instance.games_color = count_color[i]
        instance.record = record_stats[i]
        instance.record_color = record_color[i]
        instance.first = season_stats[i]
        instance.first_color = season_color[i]
        instance.latest = latest_stats[i]
        instance.latest_color = latest_color[i]

    else:
        entry = dict()
        entry['index'] = i
        entry['games'] = count_stats[i]
        entry['games_color'] = count_color[i]
        entry['record'] = record_stats[i]
        entry['record_color'] = record_color[i]
        entry['first'] = season_stats[i]
        entry['first_color'] = season_color[i]
        entry['latest'] = latest_stats[i]
        entry['latest_color'] = latest_color[i]

        instance = TableData.objects.create(**entry)
    
    instance.save()
    if (i % 1000 == 0):
        print(f'entry #{i}')

print('Compiled table data')
