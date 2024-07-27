from django.db import models

# Create your models here.
class Game (models.Model):
    opponent = models.CharField(max_length=30)
    msu_score = models.IntegerField()
    opp_score = models.IntegerField()
    home = models.CharField(max_length=1)
    season = models.IntegerField()
    date = models.DateField()
    day = models.CharField(max_length=10)
    conference = models.CharField(max_length=30)
    msu_rank = models.IntegerField(default=0)
    opp_rank = models.IntegerField(default=0)
    win = models.CharField(max_length=1)

    def __str__(self):
        return str(self.date)
    
class ScorePair (models.Model):
    index = models.IntegerField()
    high = models.IntegerField()
    low = models.IntegerField()
    games = models.IntegerField(default=0)
    first_game = models.DateField()
    last_game = models.DateField()
    record = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.high}-{self.low}'
    
class TableData (models.Model):
    index = models.IntegerField()
    games = models.IntegerField()
    games_color = models.CharField(max_length=20)
    record = models.FloatField()
    record_color = models.CharField(max_length=20)
    first = models.IntegerField()
    first_color = models.CharField(max_length=20)
    latest = models.IntegerField()
    latest_color = models.CharField(max_length=20)