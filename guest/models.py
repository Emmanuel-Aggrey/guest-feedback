from django.db import models
from base.models import BaseModel
from outlets.models import Comment
from django.contrib.auth import get_user_model
# Create your models here.

from django.core.exceptions import ValidationError


class Guest(BaseModel):

    class HEAD_ABOUT:
        FACEBOOK = "facebook"
        TWITTER = "twitter"
        X = "x"
        INSTAGRAM = "instagram"
        ALL = [FACEBOOK, TWITTER, X, INSTAGRAM]

        CHOICES = [
            (FACEBOOK, "Facebook"),
            (TWITTER, "Twitter"),
            (X, "X"),
            (INSTAGRAM, "Instagram"),

        ]
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    company = models.CharField(max_length=200, null=True, blank=True)
    head_about_us = models.CharField(
        max_length=200, null=True, blank=True, choices=HEAD_ABOUT.CHOICES)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'


class Feedback(BaseModel):
    comment = models.ForeignKey(Comment, on_delete=models.PROTECT)
    guest = models.ForeignKey(Guest, on_delete=models.PROTECT)
    excellent = models.BooleanField(default=False)
    good = models.BooleanField(default=False)
    fair = models.BooleanField(default=False)
    poor = models.BooleanField(default=False)
    staff_to_recommend = models.CharField(max_length=200, null=True, blank=True)
    comments = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.comment.name

    def clean(self):
        fields = [self.excellent, self.good, self.fair, self.poor]
        if sum(fields) != 1:
            raise ValidationError(
                "Only one of excellent, good, fair, or poor can be true at a time"
            )


class Attachment(models.Model):
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE)
    attachment = models.ImageField(upload_to='feedbacks')
