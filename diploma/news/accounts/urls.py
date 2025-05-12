from django.urls import path
from accounts.views import RegisterView, UserDetailView, UserChangeView, UserPasswordChangeView, login_view
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('account/<int:id>/', UserDetailView.as_view(), name='detail'),
    path('account/<int:id>/edit/', UserChangeView.as_view(), name='edit'),
    path('password-edit/', UserPasswordChangeView.as_view(), name='password_edit'),
]
