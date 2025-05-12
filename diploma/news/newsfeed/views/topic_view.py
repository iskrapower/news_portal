from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView, DeleteView
from newsfeed.forms import TopicForm
from newsfeed.models import Topic
from django.urls import reverse


class TopicCreateView(CreateView):
    model = Topic
    template_name = 'topic/create.html'
    form_class = TopicForm

    def form_valid(self, form):
        article = get_object_or_404(Article, id=self.kwargs.get('id'))
        comment = form.save(commit=False)
        comment.article = article
        comment.author = self.request.user
        comment.save()
        return redirect('newsfeed:article_view', id=article.id)



class TopicUpdateView(UpdateView):
    model = Topic
    template_name = 'topic/update.html'
    form_class = TopicForm
    context_object_name = 'topic'
    pk_url_kwarg = 'topic_id'

    def get_success_url(self):
        return reverse('newsfeed:article_view', kwargs={'id': self.object.article.id})


class TopicDeleteView(DeleteView):
    model = Topic
    pk_url_kwarg = 'comment_id'

    def get(self, request, *args, **kwargs):
        return self.delete(request)
    
    def get_success_url(self):
        return reverse('newsfeed:article_view', kwargs={'id': self.object.article.id})
