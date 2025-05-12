from django.shortcuts import redirect
from newsfeed.models import Article
from newsfeed.forms import ArticleForm, SimpleSearchForm
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils.http import urlencode 
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
    

class IndexView(ListView):
    model = Article
    template_name = 'article/index.html'
    context_object_name = 'articles'
    paginate_by = 5
    paginate_orphans = 1
    
    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = Q(title__icontains=self.search_value) | Q(author__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset
    
    def get_search_form(self):
        return SimpleSearchForm(self.request.GET)
    
    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None

class ArticleView(DetailView):
    template_name = 'article/detail.html'
    model = Article
    pk_url_kwarg = 'id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.object
        comments = article.comments.order_by('-published_at')
        context['comments'] = comments
        topics = article.topics.all()
        context['topics'] = topics 
        return context


class ArticleCreateView(LoginRequiredMixin, CreateView):
    template_name = 'article/create.html'
    model = Article
    form_class = ArticleForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('newsfeed:article_detail', kwargs={'id': self.object.id})


class ArticleUpdateView(PermissionRequiredMixin, UpdateView):
    model = Article
    template_name = 'article/update.html'
    form_class = ArticleForm
    context_object_name = 'article'
    pk_url_kwarg = 'id'
    permission_required = 'newsfeed.add_article'

    def has_permission(self):
        return super().has_permission() or self.get_object().author == self.request.user

    def get_success_url(self):
        return reverse('newsfeed:article_view', kwargs={'id': self.object.id})


class ArticleDeleteView(DeleteView):
    template_name = 'article/delete.html'
    model = Article
    context_object_name = 'article'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('newsfeed:article_list')
