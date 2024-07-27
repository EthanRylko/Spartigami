from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import ScorePair, Game, TableData

ROWS = 50
COLS = 104
EXCLUDE_LIST = [1, 2, 4, 7, 11, 16, 29]

table_data = dict()


def index(request):
    compile_data()

    return render(request, 'index.html', {'head_range' : range(COLS), 'row_range' : range(ROWS),
                                          'exclude_list' : EXCLUDE_LIST, 'data' : table_data['count_stats']})


def compile_data():
    table = TableData.objects.order_by('index')
    count_stats = list()
    count_color = list()
    record_stats = list()
    record_color = list()
    season_stats = list()
    season_color = list()
    latest_stats = list()
    latest_color = list()

    for item in table:
        count_stats.append(item.games)
        count_color.append(item.games_color)
        record_stats.append(item.record)
        record_color.append(item.record_color)
        season_stats.append(item.first)
        season_color.append(item.first_color)
        latest_stats.append(item.latest)
        latest_color.append(item.latest_color)

    table_data['count_stats'] = count_stats
    table_data['count_color'] = count_color
    table_data['record_stats'] = record_stats
    table_data['record_color'] = record_color
    table_data['season_stats'] = season_stats
    table_data['season_color'] = season_color
    table_data['latest_stats'] = latest_stats
    table_data['latest_color'] = latest_color

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
            
        elif mode == 'first':
            stats = table_data['season_stats']
            color = table_data['season_color']
        
        else: # mode == 'latest'
            stats = table_data['latest_stats']
            color = table_data['latest_color']

        data['stats'] = stats
        data['color'] = color

        return JsonResponse(data)
    except ScorePair.DoesNotExist:
        return JsonResponse({'error': 'Data not found'}, status=404) 