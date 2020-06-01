from .cammodelrequests import urls as cammodelrequest_urls
from .supoperators import urls as supoperator_urls
from .supcammodels import urls as supcammodel_urls
from .accounting import urls as accounting_urls
from .cammodels import urls as cammodel_urls
from .operators import urls as operator_urls
from django.urls import path, include
from . import views

app_name = 'management'

urlpatterns = [
    path('', views.Management.as_view(), name='index'),
    path('cammodel/', include(cammodel_urls, namespace='cammodel')),
    path('supcammodel/', include(supcammodel_urls, namespace='supcammodel')),
    path('cammodelrequest/', include(cammodelrequest_urls, namespace='cammodelrequest')),
    path('operator/', include(operator_urls, namespace='operator')),
    path('supoperator/', include(supoperator_urls, namespace='supoperator')),
    path('accounting/', include(accounting_urls, namespace='accounting')),
]