from django.urls import path
from common import views

app_name = 'common'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('model_request/', views.ModelRequest.as_view(), name='model_request')
]
