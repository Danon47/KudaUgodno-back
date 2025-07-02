from drf_spectacular.utils import OpenApiExample, OpenApiResponse
from rest_framework.serializers import CharField, Serializer


class MailingErrorSerializer(Serializer):
    detail = CharField()


MAILING_ID_ERROR = "Рассылка не найдена, введён неверный ID рассылки."
MAILING_EMAIL_ERROR = "Этот email уже зарегистрирован."
MAILING_400 = OpenApiResponse(
    response=MailingErrorSerializer,
    description="Ошибка валидации",
    examples=[
        OpenApiExample(
            name="Ошибка: Email уже есть в БД",
            value={"email": [MAILING_EMAIL_ERROR]},
            response_only=True,
        )
    ],
)
MAILING_404 = OpenApiResponse(
    response=MailingErrorSerializer,
    description="Рассылка не найдена",
    examples=[
        OpenApiExample(
            name="Ошибка: Рассылка не найдена",
            value={"detail": MAILING_ID_ERROR},
            response_only=True,
        )
    ],
)
