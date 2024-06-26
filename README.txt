API для аутентификации и управления профилями пользователей
1. Аутентификация пользователя
URL: /auth/
Метод: POST
Параметры запроса:
'email' (строка) - электронная почта пользователя.
Описание: Этот эндпоинт используется для аутентификации пользователя. После отправки запроса на этот URL с электронной почтой пользователя, на указанный адрес будет отправлен код подтверждения.

2. Подтверждение аутентификации
URL: /auth/<user_email>/<session_id>/
Метод: POST
Параметры запроса:
'code' (строка) - код подтверждения, полученный на электронную почту пользователя.
Описание: Этот эндпоинт используется для подтверждения аутентификации пользователя. Пользователь должен ввести код подтверждения, который был отправлен на его электронную почту.

3. Получение профиля пользователя
URL: /profile/<user_email>/
Метод: GET
Параметры запроса:
'user_email' (строка) - электронная почта пользователя.
Описание: Этот эндпоинт используется для получения профиля пользователя по его электронной почте.

4. Ввод реферального кода
URL: /enter_referral/<user_email>/
Метод: POST
Параметры запроса:
'code' (строка) - реферальный код, предоставленный другим пользователем.
Описание: Этот эндпоинт используется для ввода реферального кода другого пользователя.

5. Получение рефералов пользователя
URL: /user_referrals/<user_email>/
Метод: GET
Параметры запроса:
'user_email' (строка) - электронная почта пользователя.
Описание: Этот эндпоинт используется для получения списка рефералов пользователя по его электронной почте.

