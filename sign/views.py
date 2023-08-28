import random

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from django.views.generic import CreateView, View, FormView
from .models import MyUser, OneTimeCode
from .forms import BaseRegisterForm, VerifiedCodeForm
from .token import account_activation_token
from .utils import usual_login_view


class BaseRegisterView(CreateView):
    '''Представление формы регистрации нового пользователя'''
    model = MyUser
    form_class = BaseRegisterForm
    success_url = '/sign/signup/verified_code_page/'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = BaseRegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                verified_code = OneTimeCode.objects.create(code=random.choice('1234567890'), user=user)
                request.session['username'] = f'{user.username}'
                send_mail(
                        subject='Hello',
                        message=f'Hello, {user.username}. Введите код подтверждения. <h2>{verified_code.code}</h2>',
                        from_email='Lafen55@yandex.ru',
                        recipient_list=[form.cleaned_data.get('email')]
                    )
                return redirect('verified_code_page/')
        else:
            form = BaseRegisterForm()
        return render(request, 'sign/signup.html', {'form': form})


class InvalidCodeView(View):
    '''Представление страницы при неверно введенном коде подтверждения'''
    template_name = 'sign/invalid_code_page.html'


class RegistrationComplite(View):
    '''Представление страницы при успешной регистрации пользователя'''
    template_name = 'sign/registration_complite.html'


class VerifiedCodeView(FormView):
    '''Представление страницы для ввода кода подтверждения при завершении регистрации'''
    template_name = 'sign/verified_code_page.html'
    form_class = VerifiedCodeForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            username = request.session.get('username', 0)
            user = MyUser.objects.get(username=username)
            code_in_database = OneTimeCode.objects.get(user=user).code
            form = VerifiedCodeForm(request.POST)
            if form.is_valid():
                code_in_field = form.cleaned_data.get("verified_fieid")
                if code_in_field == code_in_database:
                    user.is_active = True
                    user.save()
                    return render(request, 'sign/registration_complite.html')
                else:
                    return render(request, 'sign/invalid_code_page.html')
        else:
            form = VerifiedCodeView()
        return render(request, 'sign/verified_code_page.html', {'form': form})

