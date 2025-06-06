from django.core.mail import EmailMessage
from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from all_fixture.fixture_views import MAILING_ID, MAILING_SETTINGS, limit, offset
from config.settings import EMAIL_HOST_USER
from mailings.models import Mailing
from mailings.serializers import MailingErrorIdSerializer, MailingSerializer


@extend_schema(tags=[MAILING_SETTINGS["name"]])
@extend_schema_view(
    list=extend_schema(
        summary="Список рассылок",
        description="Получение списка всех рассылок",
        parameters=[limit, offset],
        responses={200: MailingSerializer(many=True)},
    ),
    create=extend_schema(
        summary="Добавление рассылки на главной странице",
        description="Добавление и отправка рассылки в письме на главной странице",
        request={"multipart/form-data": MailingSerializer},
        responses={
            201: MailingSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
        },
    ),
    retrieve=extend_schema(
        summary="Детальная информация о рассылке",
        description="Получение полной информации о конкретном рассылке по ID",
        parameters=[MAILING_ID],
        responses={
            200: MailingSerializer,
            404: OpenApiResponse(response=MailingErrorIdSerializer, description="Рассылка не найдена"),
        },
    ),
    update=extend_schema(
        summary="Полное обновление парамет рассылки на главной странице",
        description="Обновление всех полей рассылки на главной странице",
        request={"multipart/form-data": MailingSerializer},
        parameters=[MAILING_ID],
        responses={
            200: MailingSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(response=MailingErrorIdSerializer, description="Рассылка не найдена"),
        },
    ),
    partial_update=extend_schema(
        summary="Частичное обновление параметров рассылки",
        description="Обновление поля 'mailing' в рассылке",
        request={"multipart/form-data": MailingSerializer},
        parameters=[MAILING_ID],
        responses={
            200: MailingSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(response=MailingErrorIdSerializer, description="Рассылка не найдена"),
        },
    ),
    destroy=extend_schema(
        summary="Удаление рассылки на главной странице",
        description="Рассылка неактивна",
        parameters=[MAILING_ID],
        responses={
            204: OpenApiResponse(description="Рассылка отключена"),
            404: OpenApiResponse(response=MailingErrorIdSerializer, description="Рассылка не найдена"),
        },
    ),
)
class MailingViewSet(viewsets.ModelViewSet):
    """ViewSet для рассылки писем туристам на главной странице."""

    permission_classes = [AllowAny]
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer

    def create(self, request, *args, **kwargs):
        """Добавление рассылки."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        email = serializer.data["email"]
        try:
            email_message = EmailMessage(
                subject="Вы подписались на рассылку",
                body="""
                    <html>
                        <body>
                            <p>Вы подписались на рассылку в сервис <strong>'Куда Угодно'</strong>:</p>
                            <p>Если вы не подписывались, то сообщите в поддержку.</p>
                        </body>
                    </html>
                """,
                from_email=EMAIL_HOST_USER,
                to=[email],
            )
            email_message.content_subtype = "html"
            email_message.send()
            return Response(
                {"message": "Спасибо за подписку!", "data": serializer.data},
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """Мягкое удаление рассылки."""
        instance = self.get_object()
        instance.mailing = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
