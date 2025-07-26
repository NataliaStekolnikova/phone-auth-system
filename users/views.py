from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.db import IntegrityError
from drf_spectacular.utils import extend_schema, OpenApiExample
from drf_spectacular.openapi import OpenApiParameter, OpenApiTypes
import random
import time
from .models import User, PhoneVerification
from django.contrib.auth import login

@extend_schema(
    tags=['Authentication'],
    summary='Отправка SMS-кода верификации',
    description='''
    Отправляет 4-значный код верификации на указанный номер телефона.
    
    **Особенности:**
    - Имитация задержки SMS (1-2 секунды)
    - Генерация случайного 4-значного кода
    - Сохранение кода в базе данных
    - Поддержка международных номеров
    
    **Для тестирования:** код возвращается в ответе (в продакшене отправляется по SMS)
    ''',
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'phone_number': {
                    'type': 'string',
                    'description': 'Номер телефона в международном формате',
                    'example': '+375294567892'
                }
            },
            'required': ['phone_number']
        }
    },
    responses={
        200: {
            'description': 'SMS-код успешно отправлен',
            'content': {
                'application/json': {
                    'example': {
                        'message': 'Код отправлен на номер',
                        'phone_number': '+375294567892',
                        'verification_code': '1234'
                    }
                }
            }
        },
        400: {
            'description': 'Ошибка валидации',
            'content': {
                'application/json': {
                    'example': {
                        'error': 'Номер телефона обязателен'
                    }
                }
            }
        }
    },
    examples=[
        OpenApiExample(
            'Белорусский номер',
            value={'phone_number': '+375294567892'},
            request_only=True,
        ),
        OpenApiExample(
            'Российский номер',
            value={'phone_number': '+79161234567'},
            request_only=True,
        ),
    ]
)
@api_view(['POST'])
@permission_classes([AllowAny])
def send_verification_code(request):
    phone_number = request.data.get('phone_number')
    
    if not phone_number:
        return Response({
            'error': 'Номер телефона обязателен'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    verification_code = str(random.randint(1000, 9999))
    time.sleep(random.uniform(1, 2))
    
    PhoneVerification.objects.create(
        phone_number=phone_number,
        verification_code=verification_code
    )
    
    return Response({
        'message': 'Код отправлен на номер',
        'phone_number': phone_number,
        'verification_code': verification_code  
    }, status=status.HTTP_200_OK)


@extend_schema(
    tags=['Authentication'],
    summary='Верификация SMS-кода и авторизация',
    description='''
    Проверяет SMS-код и выполняет авторизацию или регистрацию пользователя.
    
    **Процесс:**
    1. Проверка кода верификации
    2. Создание пользователя (если новый номер)
    3. Генерация токена авторизации
    4. Возврат данных пользователя
    
    **Токен** можно использовать для всех защищенных endpoints
    ''',
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'phone_number': {
                    'type': 'string',
                    'description': 'Номер телефона из предыдущего шага',
                    'example': '+375294567892'
                },
                'verification_code': {
                    'type': 'string',
                    'description': '4-значный код из SMS',
                    'example': '1234'
                }
            },
            'required': ['phone_number', 'verification_code']
        }
    },
    responses={
        200: {
            'description': 'Успешная авторизация',
            'content': {
                'application/json': {
                    'example': {
                        'message': 'Успешная авторизация',
                        'token': 'abc123def456789...',
                        'user_id': 1,
                        'phone_number': '+375294567892',
                        'invite_code': 'ABC123',
                        'is_new_user': True
                    }
                }
            }
        },
        400: {
            'description': 'Неверный код или отсутствующие данные',
            'content': {
                'application/json': {
                    'example': {
                        'error': 'Неверный код'
                    }
                }
            }
        }
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def verify_code(request):
    phone_number = request.data.get('phone_number')
    verification_code = request.data.get('verification_code')
    
    if not phone_number or not verification_code:
        return Response({
            'error': 'Номер телефона и код обязательны'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        phone_verification = PhoneVerification.objects.filter(
            phone_number=phone_number,
            verification_code=verification_code,
            is_verified=False
        ).latest('created_at')
    except PhoneVerification.DoesNotExist:
        return Response({
            'error': 'Неверный код'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    phone_verification.is_verified = True
    phone_verification.save()
    
    user, created = User.objects.get_or_create(
        phone_number=phone_number 
    )
    token, _ = Token.objects.get_or_create(user=user)
    
    return Response({
        'message': 'Успешная авторизация',
        'token': token.key,
        'user_id': user.id,
        'phone_number': user.phone_number,
        'invite_code': user.invite_code,
        'is_new_user': created
    }, status=status.HTTP_200_OK)


@extend_schema(
    tags=['Users'],
    summary='Получение профиля пользователя',
    description='''
    Возвращает информацию о текущем пользователе и его рефералах.
    
    **Данные профиля:**
    - Основная информация пользователя
    - Уникальный инвайт-код
    - Активированный инвайт-код (если есть)
    - Список рефералов с датами регистрации
    - Общее количество рефералов
    
    **Требуется авторизация:** токен в заголовке Authorization
    ''',
    responses={
        200: {
            'description': 'Профиль пользователя',
            'content': {
                'application/json': {
                    'example': {
                        'user_id': 1,
                        'phone_number': '+375294567892',
                        'invite_code': 'ABC123',
                        'activated_invite_code': 'XYZ789',
                        'referrals': [
                            {
                                'phone_number': '+375291234567',
                                'joined_date': '2025-07-26T10:30:00Z'
                            }
                        ],
                        'referrals_count': 1
                    }
                }
            }
        },
        401: {
            'description': 'Не авторизован',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'Authentication credentials were not provided.'
                    }
                }
            }
        }
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    user = request.user
    referrals = user.get_referrals()
    
    return Response({
        'user_id': user.id,
        'phone_number': user.phone_number,
        'invite_code': user.invite_code,
        'activated_invite_code': user.activated_invite_code,
        'referrals': [
            {
                'phone_number': ref.phone_number,
                'joined_date': ref.created_at
            } for ref in referrals
        ],
        'referrals_count': referrals.count()
    }, status=status.HTTP_200_OK)


@extend_schema(
    tags=['Referrals'],
    summary='Активация инвайт-кода',
    description='''
    Активирует инвайт-код другого пользователя.
    
    **Ограничения:**
    - Каждый пользователь может активировать только один инвайт-код
    - Нельзя активировать собственный инвайт-код
    - Инвайт-код должен существовать в системе
    
    **Эффект:** пользователь становится рефералом владельца инвайт-кода
    ''',
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'invite_code': {
                    'type': 'string',
                    'description': '6-значный инвайт-код другого пользователя',
                    'example': 'ABC123'
                }
            },
            'required': ['invite_code']
        }
    },
    responses={
        200: {
            'description': 'Инвайт-код успешно активирован',
            'content': {
                'application/json': {
                    'example': {
                        'message': 'Инвайт-код успешно активирован',
                        'activated_invite_code': 'ABC123',
                        'inviter_phone': '+375294567892'
                    }
                }
            }
        },
        400: {
            'description': 'Ошибка валидации',
            'content': {
                'application/json': {
                    'examples': {
                        'already_activated': {
                            'summary': 'Уже активирован',
                            'value': {
                                'error': 'Вы уже активировали инвайт-код: XYZ789'
                            }
                        },
                        'own_code': {
                            'summary': 'Собственный код',
                            'value': {
                                'error': 'Нельзя активировать собственный инвайт-код'
                            }
                        },
                        'not_exists': {
                            'summary': 'Не существует',
                            'value': {
                                'error': 'Инвайт-код не существует'
                            }
                        }
                    }
                }
            }
        },
        401: {
            'description': 'Не авторизован'
        }
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def activate_invite_code(request):
    invite_code = request.data.get('invite_code')
    user = request.user
    
    if not invite_code:
        return Response({
            'error': 'Инвайт-код обязателен'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if user.activated_invite_code:
        return Response({
            'error': f'Вы уже активировали инвайт-код: {user.activated_invite_code}'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if invite_code == user.invite_code:
        return Response({
            'error': 'Нельзя активировать собственный инвайт-код'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        inviter = User.objects.get(invite_code=invite_code)
    except User.DoesNotExist:
        return Response({
            'error': 'Инвайт-код не существует'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user.activated_invite_code = invite_code
    user.save()
    
    return Response({
        'message': 'Инвайт-код успешно активирован',
        'activated_invite_code': invite_code,
        'inviter_phone': inviter.phone_number
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def drf_login(request):
    """
    Специальный endpoint для логина через DRF browsable API
    Позволяет авторизоваться с токеном для тестирования в браузере
    """
    token = request.data.get('token')
    
    if not token:
        return Response({
            'error': 'Токен обязателен',
            'help': 'Введите токен из verify-code endpoint'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        
        # Логиним пользователя в сессию для DRF browsable API
        login(request, user)
        
        return Response({
            'message': 'Успешный вход в DRF интерфейс',
            'user': user.phone_number,
            'invite_code': user.invite_code,
            'info': 'Теперь можете тестировать защищенные endpoint\'ы'
        }, status=status.HTTP_200_OK)
        
    except Token.DoesNotExist:
        return Response({
            'error': 'Неверный токен',
            'help': 'Получите токен через /api/users/verify-code/'
        }, status=status.HTTP_400_BAD_REQUEST)