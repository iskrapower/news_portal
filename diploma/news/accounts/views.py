from django.shortcuts import redirect
from django.contrib.auth import login
from accounts.forms import MyUserCreationForm, UserChangeForm, ProfileChangeForm, PasswordChangeForm
from django.views.generic import CreateView, UpdateView
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.views.generic import DetailView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from accounts.models import Profile
from django.urls import reverse
from django.http import HttpResponseRedirect


def login_view(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('newsfeed:article_list')
        else:
            context['has_error'] = True
    return render(request, 'accounts/login.html', context=context)


class RegisterView(CreateView):
    model = get_user_model()
    template_name = 'accounts/register.html'
    form_class = MyUserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        user.save()
        Profile.objects.create(user=user)

        return redirect(self.get_success_url())
    
    def get_success_url(self):
        return self.request.POST.get(
            'next',
            self.request.GET.get('next', '')
        )


class UserDetailView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'accounts/detail.html'
    context_object_name = 'user_obj'
    pk_url_kwarg = 'id'
    paginate_related_by = 5
    paginate_related_orphans = 0

    def get_context_data(self, **kwargs):
        articles = self.object.articles.order_by('-created_at')
        paginator = Paginator(articles, self.paginate_related_by, orphans=self.paginate_related_orphans)
        page_number = self.request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        kwargs['page_obj'] = page
        kwargs['articles'] = page.object_list
        kwargs['is_paginated'] = page.has_other_pages()
        return super().get_context_data(**kwargs)
    

class UserChangeView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = UserChangeForm
    template_name = 'accounts/user/edit.html'
    context_object_name = 'user_obj'

    def get_context_data(self, **kwargs):
        if 'profile_form' not in kwargs:
            kwargs['profile_form'] = self.get_profile_form()
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        profile_form = self.get_profile_form()
        if form.is_valid() and profile_form.is_valid():
            return self.form_valid(form, profile_form)
        else:
            return self.form_invalid(form, profile_form)

    def form_valid(self, form, profile_form):
        response = super().form_valid(form)
        profile_form.save()
        return response

    def form_invalid(self, form, profile_form):
        context = self.get_context_data(form=form, profile_form=profile_form)
        return self.render_to_response(context)

    def get_profile_form(self):
        form_kwargs = {'instance': self.object.profile}
        if self.request.method == 'POST':
            form_kwargs['data'] = self.request.POST
            form_kwargs['files'] = self.request.FILES
        return ProfileChangeForm(**form_kwargs)
    
    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('accounts:detail', kwargs={'id': self.object.id})


class UserPasswordChangeView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'accounts/user/password_change.html'
    form_class = PasswordChangeForm
    context_object_name = 'user_obj'

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        return HttpResponseRedirect(self.get_success_url())

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('accounts:detail', kwargs={'id': self.object.id})


