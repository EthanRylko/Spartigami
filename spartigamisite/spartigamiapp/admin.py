from django.contrib import admin
from .models import Game, ScorePair, TableData

# Register your models here.
admin.site.register(Game)
admin.site.register(ScorePair)
admin.site.register(TableData)