from django.shortcuts import render
from guest.models import Guest, Feedback, Attachment
from guest.serializers import GuestSerializer, FeedbackSerializer, AttachmentSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from django.db.models import Count, Sum, Q, F
from rest_framework.response import Response
from rest_framework import status
from django_filters import rest_framework as filters
from rest_framework import generics

from rest_framework.views import APIView
# Create your views here.


class GuestViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Guest.objects.order_by("-updated_at")
    serializer_class = GuestSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'company', 'head_about_us']


class AttachmentViewSet(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Attachment.objects.order_by('id')
    serializer_class = AttachmentSerializer


class FeedbackViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = Feedback.objects.order_by("-updated_at")
    serializer_class = FeedbackSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['comment', 'excellent', 'good', 'fair', 'poor',]


class FeedbackStatsView(APIView):

    permission_classes = [IsAuthenticated]

    class FeedbackStatsFilter(filters.FilterSet):
        start_date = filters.DateFilter()

        end_date = filters.DateFilter()

    filter_backends = [DjangoFilterBackend]
    filterset_class = FeedbackStatsFilter

    def get(self, request):
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        total_feedback = Feedback.objects.count()

        if start_date and end_date:
            feedback_queryset = Feedback.objects.filter(
                created_at__date__range=[start_date, end_date]
            )
            total_feedback = feedback_queryset.count()

        stats = self.get_stats(start_date, end_date)

        stats["total_feedback"] = total_feedback

        feedback_stats = self.get_guest_feedback_stats(start_date, end_date)
        comment_feedback_stats = self.get_comment_feedback_stats(start_date, end_date)

        data = {
            "stats": stats,
            "feedback_stats": feedback_stats,
            "comment_feedback_stats": comment_feedback_stats
        }

        return Response(data, status=status.HTTP_200_OK)

    def get_stats(self, start_date=None, end_date=None):
        filters = {}
        if start_date and end_date:
            filters["created_at__date__range"] = [start_date, end_date]

        feedback_queryset = Feedback.objects.filter(**filters)

        excellent_count = feedback_queryset.filter(excellent=True).count() or 1
        good_count = feedback_queryset.filter(good=True).count() or 1
        fair_count = feedback_queryset.filter(fair=True).count() or 1
        poor_count = feedback_queryset.filter(poor=True).count() or 1

        total_count = excellent_count + good_count + fair_count + poor_count

        stats = {
            "excellent": {
                "count": excellent_count,
                "percentage": excellent_count / total_count * 100 if total_count else 0,
            },
            "good": {
                "count": good_count,
                "percentage": good_count / total_count * 100 if total_count else 0,
            },
            "fair": {
                "count": fair_count,
                "percentage": fair_count / total_count * 100 if total_count else 0,
            },
            "poor": {
                "count": poor_count,
                "percentage": poor_count / total_count * 100 if total_count else 0,
            },
        }

        return stats

    def get_guest_feedback_stats(self, start_date=None, end_date=None):
        filters = {}
        if start_date and end_date:
            filters["created_at__date__range"] = [start_date, end_date]

        feedback_queryset = Feedback.objects.filter(**filters)

        # Count of feedback submissions per guest
        feedback_per_guest = feedback_queryset.values('guest').annotate(
            total_feedback=Count('id')
        )

        # Distribution of satisfaction levels per guest
        satisfaction_per_guest = feedback_queryset.values('guest').annotate(
            excellent_count=Count('id', filter=Q(excellent=True)),
            good_count=Count('id', filter=Q(good=True)),
            fair_count=Count('id', filter=Q(fair=True)),
            poor_count=Count('id', filter=Q(poor=True))
        )

        # Calculate total feedback count
        total_feedback_count = feedback_queryset.count()

        # Calculate percentage of each satisfaction level per guest
        for stats in satisfaction_per_guest:
            total_count = sum(stats.values()) - stats['guest']
            for key in ['excellent_count', 'good_count', 'fair_count', 'poor_count']:
                stats[key.replace('_count', '_percentage')] = stats[key] / total_count * 100 if total_count else 0

        return {
            "feedback_per_guest": list(feedback_per_guest),
            "satisfaction_per_guest": list(satisfaction_per_guest),
            "total_feedback_count": total_feedback_count
        }

    def get_comment_feedback_stats(self, start_date=None, end_date=None):
        filters = {}
        if start_date and end_date:
            filters["created_at__date__range"] = [start_date, end_date]

        feedback_queryset = Feedback.objects.filter(**filters)

        # Count of feedback submissions with comments
        feedback_with_comments_count = feedback_queryset.exclude(comments='').count()

        # Get distinct comments
        distinct_comments = feedback_queryset.exclude(comments='').values_list('comments', flat=True).distinct()

        return {
            "feedback_with_comments_count": feedback_with_comments_count,
            "distinct_comments": list(distinct_comments)
        }
