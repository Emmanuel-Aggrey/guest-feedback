from django.urls import path
from outlets import views


urlpatterns = [

    path('outlets/', views.OutletViewSet.as_view())
]
