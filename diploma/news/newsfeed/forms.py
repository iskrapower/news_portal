from django import forms
from newsfeed.models import Article, Comment, Topic


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ['author']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['article', 'author']


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name', 'description']


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="Найти")
