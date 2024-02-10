from guest.models import Guest,Feedback
from rest_framework import serializers
from outlets.serializers import CommentSerializer


class GuestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Guest
        exclude = ["updated_at",'created_at']
        read_only_fields = ["id"]



class FeedbackSerializer(serializers.ModelSerializer):
    comment_obj = CommentSerializer(source='comment')
    guest_obj = GuestSerializer(source='guest')

    class Meta:
        model = Feedback
        exclude = ["updated_at",'created_at']
        read_only_fields = ["id"]
