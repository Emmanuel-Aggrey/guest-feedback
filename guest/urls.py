from guest import views
from django.urls import path

from rest_framework import routers
router = routers.DefaultRouter()


app_name = "guest"
router.register("guest", views.GuestViewSet, "guest")



router.register("feedback", views.FeedbackViewSet, "feedback")


urlpatterns = [
    path('feedback-stats/', views.FeedbackStatsView.as_view(), name='feedback_stats'),
    path('attachments/<int:pk>/', views.AttachmentViewSet.as_view(), name='attachments'),
]
urlpatterns += router.urls
