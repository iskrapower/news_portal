from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView, DeleteView
from newsfeed.forms import CommentForm
from newsfeed.models import Comment, Article
from django.urls import reverse


class ArticleCommentCreateView(CreateView):
    model = Comment
    template_name = 'comment/create.html'
    form_class = CommentForm

    def form_valid(self, form):
        article = get_object_or_404(Article, id=self.kwargs.get('id'))
        comment = form.save(commit=False)
        comment.article = article
        comment.author = self.request.user
        comment.save()
        return redirect('newsfeed:article_view', id=article.id)



class CommentUpdateView(UpdateView):
    model = Comment
    template_name = 'comment/update.html'
    form_class = CommentForm
    context_object_name = 'comment'
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse('newsfeed:article_view', kwargs={'id': self.object.article.id})


class CommentDeleteView(DeleteView):
    model = Comment
    pk_url_kwarg = 'comment_id'

    def get(self, request, *args, **kwargs):
        return self.delete(request)
    
    def get_success_url(self):
        return reverse('newsfeed:article_view', kwargs={'id': self.object.article.id})
