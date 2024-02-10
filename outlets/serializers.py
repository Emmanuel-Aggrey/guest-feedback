from outlets.models import Outlet,Comment

from rest_framework import serializers


class OutletSerializer(serializers.ModelSerializer):

    class Meta:
        model = Outlet
        fields= '__all__'
        read_only_fields = ["id"]



class CommentSerializer(serializers.ModelSerializer):
    outlet_obj = OutletSerializer()

    class Meta:
        model = Comment
        fields= '__all__'
        read_only_fields = ["id"]
