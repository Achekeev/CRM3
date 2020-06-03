from django.urls import path
from . import views

app_name = 'pair'

urlpatterns = [
    path('', views.PairList.as_view(), name='index'),
    path('create/', views.PairCreate.as_view(), name='create'),
    path('edit/<int:pk>', views.PairCreate.as_view(), name='edit'),
    path('remove/<int:pk>', views.pair_remove, name='remove')
]