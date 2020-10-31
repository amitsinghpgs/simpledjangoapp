from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth import login, authenticate
from .forms import SignupForm, PasswordResetForm
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from django.contrib.auth.models import User


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string(
                'registration/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token': default_token_generator.make_token(user),
                })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse(
                'Please confirm your email address to complete the registration')
    form = SignupForm()
    context = {
            'form': form,
            'render_login_signup' : True,
            'login_class': 'inactive underlineHover',
            'sign_up_class': 'active'}
    return render(request, 'registration/login.html', context)


def view_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse(
            'Thank you for your email confirmation. Now you can login your account.')
    return HttpResponse('Activation link is invalid!')


class LoginView(auth_views.LoginView):
    template_name = 'registration/login.html'

    def get(self, request):
        context = {
            'form': self.form_class,
            'render_login_signup' : True,
            'login_class': 'active',
            'sign_up_class': 'inactive underlineHover'}
        return render(request, self.template_name, context)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('view_quote')
        context = {'form': self.form_class}
        return render(request, self.template_name, context)


class LogoutView(auth_views.LogoutView):
    def get(self, request):
        from django.core.mail import send_mail
        return redirect('view_quote')


class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'registration/login.html'
    form_class = PasswordResetForm

    def get(self, request):
        context = {'form': self.form_class,
        'render_login': True}
        return render(request, self.template_name, context)

    def post(self, request):
        form = PasswordResetForm(request.POST)
        user = User.objects.get(username=form['username'].value(),
                                email=form['email'].value())
        current_site = get_current_site(request)
        mail_subject = 'Reset your password.'
        message = render_to_string(
            'registration/password_reset_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': default_token_generator.make_token(user),
            })
        to_email = form['email'].value()
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        return HttpResponse('Please check your email to rest password')


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('view_login')