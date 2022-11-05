from django import forms
from core import models
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = models.FeedbackModel
        # fields = "__all__" #["name", "message", "email", ]
        exclude = ('status', )
