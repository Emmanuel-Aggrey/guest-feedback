from outlets.models import Outlet, Comment

from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'


class OutletSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, source='comment_set')
    outlet = serializers.CharField(source='name')

    class Meta:
        model = Outlet
        fields = ['id', 'outlet', 'comments']
        read_only_fields = ["id"]
