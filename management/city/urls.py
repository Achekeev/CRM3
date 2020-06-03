from django.urls import path
from . import views

app_name = 'city'

urlpatterns = [
    path('', views.CityList.as_view(), name='index'),
    path('create/', views.CityCreate.as_view(), name='create'),
    path('edit/<int:pk>', views.CityCreate.as_view(), name='edit'),
    path('remove/<int:pk>', views.city_remove, name='remove')
]