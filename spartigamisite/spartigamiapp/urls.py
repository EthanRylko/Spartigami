from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/cell-data/<int:cell_id>/', views.get_cell_data, name='get_cell_data'),
    #path('api/game-data/<str:date>/', views.get_game_data, name='get_game_data'),
]