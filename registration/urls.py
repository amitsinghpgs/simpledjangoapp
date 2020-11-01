from .views import (view_activate, LoginView, signup, LogoutView, PasswordResetView,
                    PasswordResetConfirmView, view_user_details, view_create_quote,
                    view_my_quotes)
from django.urls import include, path

urlpatterns = [
    path('login/', LoginView.as_view(), name='view_login'),
    path('signup/', signup, name='view_signup'),
    path('activate/(<uidb64>)/<token>', view_activate, name='view_activate'),
    path('logout/', LogoutView.as_view(), name='view_logout'),
    path('passwordreset/', PasswordResetView.as_view(), name='view_passreset'),
    path('reset/<uidb64>/<token>',
         PasswordResetConfirmView.as_view(),
         name='view_enter_new_password'),
    path('user_details/', view_user_details, name='view_user_details'),
    path('create_quote/', view_create_quote, name='view_create_quote'),
    path('my_quotes/', view_my_quotes, name='view_my_quotes')
]