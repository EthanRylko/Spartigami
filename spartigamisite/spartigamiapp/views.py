from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import ScorePair, Game

ROWS = 50
COLS = 104

def index(request):
    score_pairs = ScorePair.objects.all()
    games_count_mode = False
    data = list()
    bgcolor = list()
    exclude_list = [1, 2, 4, 7, 11, 16, 29]

    if games_count_mode:
        max_games = ScorePair.objects.order_by('-games')[0].games

        for c in range(COLS + 1):
            for r in range(c + 1):
                try:
                    entry = score_pairs.get(high = c, low = r)
                    data.append(entry.games)

                    scalar = (max_games - entry.games) / max_games
                    scalar = scalar ** 2
                    r = 0 + 192 * scalar
                    g = 128 + 96 * scalar

                    bgcolor.append(f'rgb({r}, {g}, {r})')
                except:
                    data.append(0)
                    index = r + c * (c + 1) // 2
                    if index not in exclude_list:
                        bgcolor.append('rgb(255, 255, 255)')
                    else:
                        bgcolor.append('rgb(0, 0, 0)')
    else:
        # record mode for now
        for c in range(COLS + 1):
            for r in range(c + 1):
                try:
                    entry = score_pairs.get(high = c, low = r)

                    w, l, t = entry.record.split('-')
                    pct = (int(w) + 0.5 * float(t)) / (int(w) + int(l) + int(t))
                    data.append('%0.3f' % pct)

                    r = min(256 * (1 - pct), 128)
                    g = min(256 * pct, 128)

                    bgcolor.append(f'rgb({r}, {g}, 0)')
                except:
                    data.append(0)
                    index = r + c * (c + 1) // 2
                    if index not in exclude_list:
                        bgcolor.append('rgb(255, 255, 255)')
                    else:
                        bgcolor.append('rgb(0, 0, 0)')
                    

    return render(request, 'index.html', {'head_range' : range(COLS), 'row_range' : range(ROWS),
                                          'data' : data, 'bgcolor' : bgcolor})


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
    
def get_game_data(request, date):
    try:
        entry = Game.objects.get(date=date)
        data = {
            'opponent': entry.opponent,
        }
        return JsonResponse(data)
    except ScorePair.DoesNotExist:
        return JsonResponse({'error': 'Data not found'}, status=404)