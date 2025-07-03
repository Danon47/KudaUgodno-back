from drf_spectacular.utils import OpenApiExample, OpenApiResponse

from all_fixture.errors.list_error import MAILING_EMAIL_ERROR, MAILING_ID_ERROR
from all_fixture.errors.serializers_error import MailingErrorSerializer

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
