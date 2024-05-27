from guest.models import Guest, Feedback, Attachment
from rest_framework import serializers
from outlets.serializers import CommentSerializer


class GuestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Guest
        exclude = ["updated_at", 'created_at']
        read_only_fields = ["id"]


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = "__all__"
        read_only_fields = ["id"]


class FeedbackSerializer(serializers.ModelSerializer):
    comment_obj = CommentSerializer(source='comment', read_only=True)
    guest_obj = GuestSerializer(source='guest', read_only=True)
    guest_obj = GuestSerializer(source='guest', read_only=True)
    attachments_obj = AttachmentSerializer(source='attachment_set', read_only=True, many=True)
    attachments = serializers.ListField(
        write_only=True,
        help_text="upload single or multiple files",
        required=False,
        child=serializers.FileField(
            max_length=10000000,
            allow_empty_file=False,
            required=False,
            use_url=False,
        ),
    )

    def create(self, validated_data):
        attachments = validated_data.pop("attachments", [])

        instance = super().create(validated_data)
        self.create_or_update_attachment(instance, attachments)
        return instance

    def update(self, instance, validated_data):
        attachments = validated_data.pop("attachments", [])
        instance = super().update(instance, validated_data)
        self.create_or_update_attachment(instance, attachments)
        return instance

    def create_or_update_attachment(self, feedback, attachments):
        if attachments:
            Attachment.objects.filter(feedback=feedback).delete()
            files_data = [
                {"feedback": feedback.id, "attachment": attachment} for attachment in attachments
            ]
            file_serializer = AttachmentSerializer(data=files_data, many=True)

            if file_serializer.is_valid(raise_exception=True):
                file_serializer.save()

    class Meta:
        model = Feedback
        exclude = ["updated_at", 'created_at']
        read_only_fields = ["id"]
