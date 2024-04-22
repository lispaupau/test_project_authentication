import os
import smtplib
import random
import string

from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from dotenv import load_dotenv
from django.shortcuts import render, redirect
from .models import UserProfile

load_dotenv()


# Реализуем получение почты юзера и отправку проверочного кода на почту
def auth_view(request):
    # Получаем почту юзера в случае POST запроса, иначе возвращаем страницу авторизации
    if request.method == 'POST':
        user_email = request.POST.get('email')
        # генерируем случайный код подтверждения
        ver_code = str(random.randint(1000, 9999))
        # отправка письма с кодом подтверждения
        with smtplib.SMTP('smtp.mail.ru') as connection:
            connection.starttls()
            connection.login(user=os.getenv('EMAIL'), password=os.getenv('PASS'))
            connection.sendmail(from_addr=os.getenv('EMAIL'), to_addrs=user_email,
                                msg=f'Subject:Verification code\n\n{ver_code}')

        # сохраняем в сессии отправленный код
        session_id = request.session.session_key
        request.session['verification_code'] = ver_code
        request.session.save()

        # редиректим юзера на страницу ввода кода подтверждения
        return redirect('verify_view', user_email=user_email, session_id=session_id)
    else:
        return render(request, 'auth.html')


# Реализуем аутентификацию юзера по коду подтверждения с почты
def verify_view(request, user_email, session_id):
    session = Session.objects.get(session_key=session_id)
    # в случае POST запроса, получаем введенный юзером код и сохраненный ранее в сессии отправленный код для сравнения
    if request.method == 'POST':
        user_code = request.POST.get('code')
        sent_code = session.get_decoded().get('verification_code')
        # проверяем введенный юзером код и получаем из сессии ранее введенную юзером почту
        if user_code == sent_code:
            user_email = user_email
            # если такая почта еще не существует в БД, то добавляем ее в БД
            if not UserProfile.objects.filter(email=user_email).exists():
                user_profile = UserProfile(email=user_email,
                                           referral_code=''.join(
                                               random.choices(string.ascii_letters + string.digits, k=6)))
                user_profile.save()
            return redirect('profile_view', user_email=user_email)
        else:
            return HttpResponse('Неверный код')
    else:
        return render(request, 'verification.html')


# после успешной авторизации возвращаем профиль пользователя с его почтой
def profile_view(request, user_email):
    try:
        user_profile = UserProfile.objects.get(email=user_email)
        return render(request, 'profile.html', {'user_profile': user_profile})
    except ObjectDoesNotExist:
        return redirect('auth_view')


# реализация реферальной системы
def referral_view(request, user_email):
    try:
        referral_user = UserProfile.objects.get(email=user_email)
    except ObjectDoesNotExist:
        return redirect('auth_view')

    if request.method == 'POST':
        # обрабатываем исключение в случае, если реферального кода не существует в БД
        try:
            code = request.POST.get('code')
            user_with_referral_code = UserProfile.objects.get(referral_code=code)
        except ObjectDoesNotExist:
            return render(request, 'enter_referral.html', {'status': 'Реферальный код не существует'})
        # проверяем юзера на возможность вводить реферальный код и возвращаем сообщение о статусе операции
        if (referral_user.activated_invite_code == 0
                and referral_user.referral_code != user_with_referral_code.referral_code):
            referral_user.referred_emails.add(user_with_referral_code)
            referral_user.activated_invite_code = True
            referral_user.save()
            return render(request, 'enter_referral.html', {'status': 'Реферальный код успешно добавлен'})
        else:
            return render(request, 'enter_referral.html',
                          {'status': 'Вы уже вводили реферальный код, либо ввели свой же код'})
    else:
        return render(request, 'enter_referral.html', {'status': 'Введите реферальный код'})


# выводим на страницу рефералов юзера по имейлу
def get_referrals_view(request, user_email):
    try:
        current_user_profile = UserProfile.objects.get(email=user_email)
        referrals = current_user_profile.referrals.all()
        return render(request, 'user_referrals.html', {'referrals': referrals})
    except ObjectDoesNotExist:
        return redirect('auth_view')
