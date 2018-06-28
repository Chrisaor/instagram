from django import forms
from django.forms import ModelForm

from posts.models import Post


class PostCreate(forms.Form):
    photo = forms.ImageField(label='사진')
    content = forms.CharField(label='남기는 말', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }
    ))

    def create_post(self, user):
        photo = self.cleaned_data['photo']
        content = self.cleaned_data['content']
        post = Post.objects.create(author=user, photo=photo, content=content)
        return post


class PostModelForm(ModelForm):

    class Meta:
        model = Post
        fields = [ 'photo', 'content']


