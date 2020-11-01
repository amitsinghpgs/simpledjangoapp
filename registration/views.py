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
from quote.forms import PatialQuoteForm
from quote.models import Quote


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
        'render_login_signup': True,
        'login_class': 'inactive underlineHover',
        'sign_up_class': 'active'
    }
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
            'render_login_signup': True,
            'login_class': 'active',
            'sign_up_class': 'inactive underlineHover'
        }
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
        context = {'form': self.form_class, 'render_login': True}
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


def view_user_details(request):
    id = request.user.id
    try:
        u = User.objects.get(pk=id)
    except User.DoesNotExist:
        u = None
    if u is None:
        return redirect('view_login')
    context = {
        'user_details': True,
        'class_user_details': 'sidelinks selected_sidelinks',
        'class_my_quotes': 'sidelinks',
        'class_create_quote': 'sidelinks',
        'fields': {
            'Username': u.username,
            'Firstname': u.first_name,
            'Lastname': u.last_name,
            'Email': u.email
        }
    }
    return render(request, 'registration/user_details.html', context)


def view_create_quote(request):
    if request.method == 'POST':
        id = request.user.id
        try:
            u = User.objects.get(pk=id)
        except User.DoesNotExist:
            u = None
        if u is None:
            return redirect('view_login')
        form = PatialQuoteForm(request.POST)
        new_quote = form.save(commit=False)
        new_quote.user = u
        new_quote.author = u
        new_quote.save()
    form = PatialQuoteForm()
    context = {
        'form': form,
        'class_user_details': 'sidelinks',
        'class_my_quotes': 'sidelinks',
        'class_create_quote': 'sidelinks selected_sidelinks',
        'create_quote': True
    }
    return render(request, 'registration/user_details.html', context)


def view_my_quotes(request):
    id = request.user.id
    try:
        u = User.objects.get(pk=id)
    except User.DoesNotExist:
        u = None
    if u is None:
        return redirect('view_login')
    all_quotes = Quote.objects.filter(user=u)

    context = {
        'all_quotes': all_quotes,
        'class_user_details': 'sidelinks',
        'class_my_quotes': 'sidelinks selected_sidelinks',
        'class_create_quote': 'sidelinks',
        'my_quotes': True
    }
    return render(request, 'registration/user_details.html', context)