from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):
    """
    Аутентификация по JWT-токену из cookie `access_token`.

    Если заголовок Authorization не передан, токен ищется в cookies.
    Поддерживает стандартную проверку токена SimpleJWT.
    """

    def authenticate(self, request):
        """
        Пытается извлечь и верифицировать JWT-токен из заголовка Authorization
        или, если он отсутствует, из cookie `access_token`.

        Возвращает пару (пользователь, токен) или None, если токен не найден.
        """
        header = self.get_header(request)
        if header is None:
            raw_token = request.COOKIES.get("access_token")
        else:
            raw_token = self.get_raw_token(header)

        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token
