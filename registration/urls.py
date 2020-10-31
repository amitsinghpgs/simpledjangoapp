from .views import view_activate, LoginView, signup, LogoutView, PasswordResetView, PasswordResetConfirmView
from django.urls import include, path

urlpatterns = [
    path('login/', LoginView.as_view(), name='view_login'),
    path('signup/', signup, name='view_signup'),
    path('activate/(<uidb64>)/<token>', view_activate, name='view_activate'),
    path('logout/', LogoutView.as_view(), name='view_logout'),
    path('passwordreset/', PasswordResetView.as_view(), name='view_passreset'),
    path('reset/<uidb64>/<token>',
         PasswordResetConfirmView.as_view(),
         name='view_enter_new_password')
]