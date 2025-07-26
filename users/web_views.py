from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import User, PhoneVerification
from rest_framework.authtoken.models import Token
import random
import time

def index_view(request):
    """Главная страница с формой ввода номера телефона"""
    return render(request, 'users/index.html')

def send_code_view(request):
    """Отправка кода подтверждения через веб-интерфейс"""
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        
        if not phone_number:
            messages.error(request, 'Номер телефона обязателен')
            return render(request, 'users/index.html')
        
        # Генерируем код (как в API)
        verification_code = str(random.randint(1000, 9999))
        time.sleep(random.uniform(1, 2))  # Имитация задержки
        
        # Сохраняем в базу
        PhoneVerification.objects.create(
            phone_number=phone_number,
            verification_code=verification_code
        )
        
        # Сохраняем в сессии для следующего шага
        request.session['phone_number'] = phone_number
        request.session['verification_code'] = verification_code
        
        messages.success(request, f'Код отправлен на номер {phone_number}')
        
        # Для демо показываем код (в реальности его отправляют по SMS)
        messages.info(request, f'Код для тестирования: {verification_code}')
        
        return render(request, 'users/verify.html', {
            'phone_number': phone_number
        })
    
    return redirect('index')

def verify_code_view(request):
    """Подтверждение кода через веб-интерфейс"""
    if request.method == 'POST':
        phone_number = request.session.get('phone_number')
        entered_code = request.POST.get('verification_code')
        
        if not phone_number or not entered_code:
            messages.error(request, 'Номер телефона и код обязательны')
            return redirect('index')
        
        try:
            phone_verification = PhoneVerification.objects.filter(
                phone_number=phone_number,
                verification_code=entered_code,
                is_verified=False
            ).latest('created_at')
        except PhoneVerification.DoesNotExist:
            messages.error(request, 'Неверный код')
            return render(request, 'users/verify.html', {
                'phone_number': phone_number
            })
        
        # Помечаем код как использованный
        phone_verification.is_verified = True
        phone_verification.save()
        
        # Создаем или получаем пользователя
        user, created = User.objects.get_or_create(phone_number=phone_number)
        token, _ = Token.objects.get_or_create(user=user)
        
        # Сохраняем в сессии
        request.session['user_id'] = user.id
        request.session['token'] = token.key
        
        if created:
            messages.success(request, f'Добро пожаловать! Ваш инвайт-код: {user.invite_code}')
        else:
            messages.success(request, 'Успешная авторизация!')
        
        return redirect('profile')
    
    # GET запрос - показываем форму
    phone_number = request.session.get('phone_number')
    if not phone_number:
        return redirect('index')
    
    return render(request, 'users/verify.html', {
        'phone_number': phone_number
    })

def profile_view(request):
    """Профиль пользователя через веб-интерфейс"""
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Необходима авторизация')
        return redirect('index')
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'Пользователь не найден')
        return redirect('index')
    
    # Обработка активации инвайт-кода
    if request.method == 'POST':
        invite_code = request.POST.get('invite_code')
        
        if not invite_code:
            messages.error(request, 'Инвайт-код обязателен')
        elif user.activated_invite_code:
            messages.error(request, f'Вы уже активировали инвайт-код: {user.activated_invite_code}')
        elif invite_code == user.invite_code:
            messages.error(request, 'Нельзя активировать собственный инвайт-код')
        else:
            try:
                inviter = User.objects.get(invite_code=invite_code)
                user.activated_invite_code = invite_code
                user.save()
                messages.success(request, f'Инвайт-код успешно активирован! Пригласил: {inviter.phone_number}')
            except User.DoesNotExist:
                messages.error(request, 'Инвайт-код не существует')
    
    # Получаем рефералов
    referrals = user.get_referrals()
    
    return render(request, 'users/profile.html', {
        'user': user,
        'referrals': referrals,
        'referrals_count': referrals.count()
    })

def logout_view(request):
    """Выход из системы"""
    request.session.flush()
    messages.success(request, 'Вы вышли из системы')
    return redirect('index')