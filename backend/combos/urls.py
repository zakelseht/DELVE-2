from django.urls import include, path
# from rest_framework import routers
from . import views
    
# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)

# serializing cytos
urlpatterns = [
    # path('router/', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),    
    path('', views.combos_class.as_view(), name='combos'),
    path('<slug:slug>/', views.combos_class.as_view()),
    path('d3', views.graph_d3),       

]