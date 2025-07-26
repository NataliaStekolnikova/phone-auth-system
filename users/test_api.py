import requests

# Получить код для первого пользователя
response1 = requests.post('http://127.0.0.1:8000/api/users/send-code/', 
                         json={'phone_number': '+375294567892'})
print('Send code response:', response1.json())
code = response1.json()['verification_code']

# Верифицировать код
response2 = requests.post('http://127.0.0.1:8000/api/users/verify-code/', 
                         json={'phone_number': '+375294567892', 'verification_code': code})
print('Verify response:', response2.json())
invite_code = response2.json().get('invite_code')
print(f'First user invite code: {invite_code}')