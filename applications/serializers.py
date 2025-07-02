import logging
from typing import Any, Dict, Type

from django.db import IntegrityError, transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from all_fixture.validators.validators import ForbiddenWordValidator
from applications.models import (
    ApplicationCancellationInsurance,
    ApplicationHotel,
    ApplicationMedicalInsurance,
    ApplicationTour,
    ApplicationVisa,
)
from guests.serializers import GuestSerializer
from hotels.serializers import HotelListWithPhotoSerializer
from rooms.serializers import RoomDetailSerializer
from tours.serializers import TourListSerializer


logger = logging.getLogger(__name__)


class ApplicationVisaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationVisa
        fields = (
            "count",
            "price",
            "total_price",
        )


class ApplicationMedicalInsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationMedicalInsurance
        fields = (
            "count",
            "price",
            "total_price",
        )


class ApplicationCancellationInsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationCancellationInsurance
        fields = ("total_price",)


class RelatedObjectsMixin:
    """Миксин для работы с связанными объектами заявок"""

    RELATED_FIELDS_MAP = {
        "visa": ApplicationVisa,
        "med_insurance": ApplicationMedicalInsurance,
        "cancellation_insurance": ApplicationCancellationInsurance,
    }

    def _create_related_objects(self, validated_data: Dict[str, Any]) -> Dict[str, Any]:
        """Создание связанных объектов и возврат словаря с созданными объектами"""
        related_objects = {}
        for field_name, model_class in self.RELATED_FIELDS_MAP.items():
            data = validated_data.pop(field_name, None)
            if data:
                try:
                    related_objects[field_name] = model_class.objects.create(**data)
                except Exception as e:
                    logger.error(f"Ошибка создания {field_name}: {str(e)}")
                    raise ValidationError({field_name: f"Ошибка создания {field_name}"})
        return related_objects

    def _update_related_object(
        self, instance: Any, validated_data: Dict[str, Any], field_name: str, model_class: Type
    ) -> None:
        """Универсальный метод для обновления связанных объектов"""
        field_data = validated_data.pop(field_name, None)
        if field_data is not None:
            related_obj = getattr(instance, field_name)
            try:
                if related_obj:
                    # Обновляем существующий объект
                    for attr, value in field_data.items():
                        setattr(related_obj, attr, value)
                    related_obj.save()
                else:
                    # Создаем новый объект и связываем с инстансом
                    new_obj = model_class.objects.create(**field_data)
                    setattr(instance, field_name, new_obj)
            except Exception as e:
                logger.error(f"Ошибка обновления {field_name}: {str(e)}")
                raise ValidationError({field_name: f"Ошибка обновления {field_name}"})

    def _update_all_related_objects(self, instance: Any, validated_data: Dict[str, Any]) -> None:
        """Обновление всех связанных объектов"""
        for field_name, model_class in self.RELATED_FIELDS_MAP.items():
            self._update_related_object(instance, validated_data, field_name, model_class)


class ApplicationBaseSerializer(RelatedObjectsMixin, serializers.ModelSerializer):
    """
    Базовая сериализация для заявок.
    Содержит общую логику для работы со связанными объектами.
    """

    wishes = serializers.CharField(validators=[ForbiddenWordValidator()], required=False, allow_blank=True)
    visa = ApplicationVisaSerializer(required=False)
    med_insurance = ApplicationMedicalInsuranceSerializer(required=False)
    cancellation_insurance = ApplicationCancellationInsuranceSerializer(required=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False)

    class Meta:
        fields = (
            "id",
            "email",
            "phone_number",
            "visa",
            "med_insurance",
            "cancellation_insurance",
            "wishes",
            "status",
            "price",
        )
        extra_kwargs = {
            "visa": {"required": False},
            "med_insurance": {"required": False},
            "cancellation_insurance": {"required": False},
            "email": {"required": True},
            "phone_number": {"required": True},
        }

    def validate_email(self, value: str) -> str:
        """Валидация email"""
        if not value or not value.strip():
            raise ValidationError("Email обязателен для заполнения")
        return value.strip()

    def validate_phone_number(self, value: str) -> str:
        """Валидация номера телефона"""
        if not value or not value.strip():
            raise ValidationError("Номер телефона обязателен для заполнения")
        return value.strip()

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Кастомная валидация данных"""
        # Проверка визы
        visa_data = data.get("visa")
        if visa_data and not visa_data.get("count"):
            raise ValidationError({"visa": "Количество виз обязательно при оформлении визы"})

        # Проверка медицинской страховки
        med_insurance_data = data.get("med_insurance")
        if med_insurance_data and not med_insurance_data.get("count"):
            raise ValidationError({"med_insurance": "Количество страховок обязательно"})

        return data

    @transaction.atomic
    def create(self, validated_data: Dict[str, Any]) -> Any:
        """
        Создание заявки с связанными объектами.

        Args:
            validated_data: Валидированные данные

        Returns:
            Созданная заявка

        Raises:
            ValidationError: При ошибке создания
        """
        guests_data = validated_data.pop("quantity_guests", [])

        try:
            # Создаем связанные объекты
            related_objects = self._create_related_objects(validated_data)
            validated_data.update(related_objects)

            # Создаем основную заявку
            application = self.Meta.model.objects.create(**validated_data)

            # Добавляем гостей если они есть
            if guests_data:
                application.quantity_guests.set(guests_data)

            return application

        except ValidationError:
            raise
        except IntegrityError as e:
            logger.error(f"Ошибка целостности данных при создании заявки: {str(e)}")
            raise ValidationError({"detail": "Конфликт данных при создании заявки"})
        except Exception as e:
            logger.error(f"Неожиданная ошибка при создании заявки: {str(e)}")
            raise ValidationError({"detail": "Произошла неожиданная ошибка при создании заявки"})

    @transaction.atomic
    def update(self, instance: Any, validated_data: Dict[str, Any]) -> Any:
        """
        Обновление заявки с связанными объектами.

        Args:
            instance: Экземпляр заявки для обновления
            validated_data: Валидированные данные

        Returns:
            Обновленная заявка

        Raises:
            ValidationError: При ошибке обновления
        """
        guests_data = validated_data.pop("quantity_guests", None)

        try:
            # Обновляем связанные объекты
            self._update_all_related_objects(instance, validated_data)

            # Обновляем основные поля
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            # Обновляем гостей если переданы
            if guests_data is not None:
                instance.quantity_guests.set(guests_data)

            instance.save()
            return instance

        except ValidationError:
            raise
        except IntegrityError as e:
            logger.error(f"Ошибка целостности данных при обновлении заявки {instance.id}: {str(e)}")
            raise ValidationError({"detail": "Конфликт данных при обновлении заявки"})
        except Exception as e:
            logger.error(f"Неожиданная ошибка при обновлении заявки {instance.id}: {str(e)}")
            raise ValidationError({"detail": "Произошла неожиданная ошибка при обновлении заявки"})


class ApplicationTourSerializer(ApplicationBaseSerializer):
    """
    Сериализатор для создания и обновления заявок на туры.
    Методы: POST, PUT, PATCH.
    """

    class Meta(ApplicationBaseSerializer.Meta):
        model = ApplicationTour
        fields = ApplicationBaseSerializer.Meta.fields + ("tour", "quantity_guests")
        extra_kwargs = {
            **ApplicationBaseSerializer.Meta.extra_kwargs,
            "tour": {"required": True},
        }

    def validate_tour(self, value):
        """Валидация тура"""
        if not value:
            raise ValidationError("Тур обязателен для заполнения")
        return value

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Расширенная валидация для заявок на туры"""
        data = super().validate(data)

        # Дополнительные проверки для туров
        guests_data = data.get("quantity_guests", [])
        if not guests_data:
            raise ValidationError({"quantity_guests": "Необходимо указать хотя бы одного гостя"})

        return data


class ApplicationTourListSerializer(ApplicationBaseSerializer):
    """
    Сериализатор для получения списка заявок на туры.
    Методы: GET.
    """

    tour = TourListSerializer(read_only=True)
    quantity_guests = GuestSerializer(many=True, read_only=True)
    visa = ApplicationVisaSerializer(read_only=True)
    med_insurance = ApplicationMedicalInsuranceSerializer(read_only=True)
    cancellation_insurance = ApplicationCancellationInsuranceSerializer(read_only=True)

    class Meta(ApplicationBaseSerializer.Meta):
        model = ApplicationTour
        fields = ApplicationBaseSerializer.Meta.fields + ("tour", "quantity_guests")
        read_only_fields = ("status", "id")

    @classmethod
    def setup_eager_loading(cls, queryset):
        """
        Метод для оптимизации запросов с предварительной загрузкой связанных объектов.

        Usage:
            queryset = ApplicationTourListSerializer.setup_eager_loading(queryset)
        """
        return queryset.select_related("visa", "med_insurance", "cancellation_insurance", "tour").prefetch_related(
            "quantity_guests"
        )


class ApplicationHotelSerializer(ApplicationBaseSerializer):
    """
    Сериализатор для создания и обновления заявок на отели.
    Методы: POST, PUT, PATCH.
    """

    class Meta(ApplicationBaseSerializer.Meta):
        model = ApplicationHotel
        fields = ApplicationBaseSerializer.Meta.fields + ("hotel", "room", "quantity_guests")
        extra_kwargs = {
            **ApplicationBaseSerializer.Meta.extra_kwargs,
            "hotel": {"required": True},
            "room": {"required": True},
        }

    def validate_hotel(self, value):
        """Валидация отеля"""
        if not value:
            raise ValidationError("Отель обязателен для заполнения")
        return value

    def validate_room(self, value):
        """Валидация номера"""
        if not value:
            raise ValidationError("Номер обязателен для заполнения")
        return value

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Расширенная валидация для заявок на отели"""
        data = super().validate(data)

        # Дополнительные проверки для отелей
        guests_data = data.get("quantity_guests", [])
        if not guests_data:
            raise ValidationError({"quantity_guests": "Необходимо указать хотя бы одного гостя"})

        # Проверка соответствия номера отелю
        hotel = data.get("hotel")
        room = data.get("room")
        if hotel and room and hasattr(room, "hotel") and room.hotel != hotel:
            raise ValidationError({"room": "Выбранный номер не принадлежит указанному отелю"})

        return data


class ApplicationHotelListSerializer(ApplicationBaseSerializer):
    """
    Сериализатор для получения списка заявок на отели.
    Методы: GET.
    """

    hotel = HotelListWithPhotoSerializer(read_only=True)
    room = RoomDetailSerializer(read_only=True)
    quantity_guests = GuestSerializer(many=True, read_only=True)
    visa = ApplicationVisaSerializer(read_only=True)
    med_insurance = ApplicationMedicalInsuranceSerializer(read_only=True)
    cancellation_insurance = ApplicationCancellationInsuranceSerializer(read_only=True)

    class Meta(ApplicationBaseSerializer.Meta):
        model = ApplicationHotel
        fields = ApplicationBaseSerializer.Meta.fields + ("hotel", "room", "quantity_guests")
        read_only_fields = ("status", "id")

    @classmethod
    def setup_eager_loading(cls, queryset):
        """
        Метод для оптимизации запросов с предварительной загрузкой связанных объектов.

        Usage:
            queryset = ApplicationHotelListSerializer.setup_eager_loading(queryset)
        """
        return queryset.select_related(
            "visa", "med_insurance", "cancellation_insurance", "hotel", "room"
        ).prefetch_related("quantity_guests")
