from django.forms import ModelForm
from .models import Subscribers, MailMessage, Comment
from froala_editor.widgets import FroalaEditor


class SubscribersForm(ModelForm):
    class Meta:
        model = Subscribers
        fields = ['email', ]


class MailMessageForm(ModelForm):
    class Meta:
        model = MailMessage
        fields = ['tilte', 'message']


class BlogForm(ModelForm):

    class Meta:
        model = Comment
        fields = [
            'name',
            'body',
        ]
