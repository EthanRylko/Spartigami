import django, os
import spartigamisite.settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spartigamisite.settings')
django.setup()

from spartigamiapp.models import Game, ScorePair

print('Hello World!')

games = Game.objects.all().order_by('date')
pairs = ScorePair.objects.all()

for game in games:
    high_score = game.msu_score if game.msu_score > game.opp_score else game.opp_score
    low_score = game.msu_score if game.msu_score < game.opp_score else game.opp_score
    score_pair_str = f'{high_score}-{low_score}'
    vs_or_at = 'vs.' if game.home == 'H' else 'at'
    msu_rank = '' if game.msu_rank == 0 else f'({game.msu_rank}) '
    opp_rank = '' if game.opp_rank == 0 else f'({game.opp_rank}) '
    day_str = f'{game.day} {game.date}'
    win = game.win

    print(f'{day_str}: {msu_rank}MSU {vs_or_at} {opp_rank}{game.opponent} {score_pair_str} {win}')

    if not ScorePair.objects.filter(high = high_score, low = low_score).exists():
        entry = dict()
        entry['index'] = low_score + high_score * (high_score + 1) // 2
        entry['high'] = high_score
        entry['low'] = low_score
        entry['games'] = 1
        entry['first_game'] = game.date
        entry['last_game'] = game.date
        entry['record'] = '1-0-0' if win == 'W' else '0-1-0'
        if win == 'T': entry['record'] = '0-0-1'

        print('Scorigami!')

        instance = ScorePair.objects.create(**entry)
        instance.save()
    else:
        entry = ScorePair.objects.get(high = high_score, low = low_score)
        entry.games = entry.games + 1
        entry.last_game = game.date
        record = entry.record
        
        # update record
        w, l, t = record.split('-')
        if win == 'W': w = str(int(w) + 1)
        if win == 'L': l = str(int(l) + 1)
        if win == 'T': t = str(int(t) + 1)
        entry.record = f'{w}-{l}-{t}'

        entry.save()

    