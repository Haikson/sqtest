from django.urls import path

from simple_content import views
from rest_framework import routers


router = routers.DefaultRouter()

router.register(r'contents', views.ContentViewSet, 'contents')

app_name = 'content_api'


urlpatterns = router.urls + [
    path('navigation/', views.NavigationView.as_view(), name='navigation_roots'),
    path('navigation/<int:current>/', views.NavigationView.as_view(), name='navigation')
]

