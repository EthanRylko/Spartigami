from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import ScorePair, Game

ROWS = 50
COLS = 104
table_data = dict()
EXCLUDE_LIST = [1, 2, 4, 7, 11, 16, 29]

def index(request):
    compile_data()

    return render(request, 'index.html', {'head_range' : range(COLS), 'row_range' : range(ROWS),
                                          'exclude_list' : EXCLUDE_LIST, 'data' : table_data['count_stats']})

def compile_data():
    score_pairs = ScorePair.objects.all()
    games = Game.objects.all()
    max_games = ScorePair.objects.order_by('-games')[0].games

    count_stats = list()
    count_color = list()
    record_stats = list()
    record_color = list()
    season_stats = list()
    season_color = list()

    for c in range(COLS + 1):
        for r in range(c + 1):
            try:
                entry = score_pairs.get(high = c, low = r)

                count_stats.append(entry.games)
                count_color.append(calc_count_color(entry.games, max_games))

                w, l, t = entry.record.split('-')
                pct = (int(w) + 0.5 * float(t)) / (int(w) + int(l) + int(t))
                record_stats.append('%0.3f' % pct)
                record_color.append(calc_record_color(pct))

                game = games.get(date = entry.first_game)
                season_stats.append(game.season)
                season_color.append(calc_season_color(int(game.season)))

            except:
                count_stats.append(0)
                record_stats.append(0)
                season_stats.append(0)
                index = r + c * (c + 1) // 2
                if index not in EXCLUDE_LIST:
                    count_color.append('rgb(255, 255, 255)')
                    record_color.append('rgb(255, 255, 255)')
                    season_color.append('rgb(255, 255, 255)')
                else:
                    count_color.append('rgb(0, 0, 0)')
                    record_color.append('rgb(0, 0, 0)')
                    season_color.append('rgb(0, 0, 0)')
    
    table_data['count_stats'] = count_stats
    table_data['count_color'] = count_color
    table_data['record_stats'] = record_stats
    table_data['record_color'] = record_color
    table_data['season_stats'] = season_stats
    table_data['season_color'] = season_color
    

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

def get_cell_data(request, cell_id):
    try:
        entry = ScorePair.objects.get(index=cell_id)
        first_game = Game.objects.get(date=entry.first_game)

        data = {
            'games': entry.games,
            'high': entry.high,
            'low': entry.low,
            'first_game': entry.first_game,
            'last_game': entry.last_game,
            'record': entry.record,
            'first_opponent': first_game.opponent,
            'first_home': first_game.home,
            'first_win': first_game.win,
            'first_day': first_game.day,
            'first_msu_rank': first_game.msu_rank,
            'first_opp_rank': first_game.opp_rank,
        }

        if entry.first_game != entry.last_game:
            last_game = Game.objects.get(date=entry.last_game)
            data['last_opponent'] = last_game.opponent
            data['last_home'] = last_game.home
            data['last_win'] = last_game.win
            data['last_day'] = last_game.day
            data['last_msu_rank'] = last_game.msu_rank
            data['last_opp_rank'] = last_game.opp_rank
        
        return JsonResponse(data)
    except ScorePair.DoesNotExist:
        return JsonResponse({'error': 'Data not found'}, status=404)
    
def refresh_table(request, mode):
    try:
        data = dict()
        stats = list()
        color = list()

        if mode == 'count':
            stats = table_data['count_stats']
            color = table_data['count_color']

        elif mode == 'record':
            stats = table_data['record_stats']
            color = table_data['record_color']
            
        else: # mode == 'season'
            stats = table_data['season_stats']
            color = table_data['season_color']

        data['stats'] = stats
        data['color'] = color

        return JsonResponse(data)
    except ScorePair.DoesNotExist:
        return JsonResponse({'error': 'Data not found'}, status=404) 