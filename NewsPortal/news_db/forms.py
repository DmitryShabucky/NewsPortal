from django import forms
# from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['category', 'title', 'text', 'author']

    # def clean(self):
    #     cleaned_data = super().clean()
    #     return cleaned_data

class CommonSignupForm(SignupForm):

    def save(self, request):
        user= super(CommonSignupForm, self).save(request)
        common_group = Group.objects.get(name= 'common')
        common_group.user_set.add(user)
        return user


