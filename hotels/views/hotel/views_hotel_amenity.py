# from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse
# from rest_framework import viewsets
#
# from all_fixture.fixture_views import tags_hotel_amenity_common_settings, tags_hotel_amenity_room_settings, \
#     tags_hotel_amenity_sport_settings, tags_hotel_amenity_children_settings
# from hotels.models.hotel.models_hotel_amenity import (
#     HotelAmenityCommon,
#     HotelAmenityForChildren,
#     HotelAmenityInTheRoom,
#     HotelAmenitySportsAndRecreation,
# )
# from hotels.serializers.hotel.serializers_hotel_amenity import (
#     HotelAmenityCommonSerializer,
#     HotelAmenityRoomSerializer,
#     HotelAmenitySportsSerializer,
#     HotelAmenityChildrenSerializer,
# )
# from hotels.views.hotel.views_hotel import CreatedByUserFilterMixin
#
#
# @extend_schema_view(
#     list=extend_schema(
#         summary="Список общих удобств в отеле",
#         description="Получение списка всех общих удобств в отеле",
#         responses={
#             200: HotelAmenityCommonSerializer(many=True),
#             400: OpenApiResponse(description="Ошибка запроса"),
#         },
#         tags=[tags_hotel_amenity_common_settings["name"]],
#     ),
#     create=extend_schema(
#         summary="Добавление общего удобства в отеле",
#         description="Создание нового общего удобства в отеле",
#         request=HotelAmenityCommonSerializer,
#         responses={
#             201: HotelAmenityCommonSerializer,
#             400: OpenApiResponse(description="Ошибка валидации"),
#         },
#         tags=[tags_hotel_amenity_common_settings["name"]],
#     ),
#     retrieve=extend_schema(
#         summary="Детали общего удобства в отеле",
#         description="Получение полной информации общего удобства в отеле",
#         responses={
#             200: HotelAmenityCommonSerializer,
#             404: OpenApiResponse(description="Общее удобство в отеле не найдено"),
#         },
#         tags=[tags_hotel_amenity_common_settings["name"]],
#     ),
#     update=extend_schema(
#         summary="Полное обновление общего удобства в отеле",
#         description="Обновление всех полей общего удобства в отеле",
#         request=HotelAmenityCommonSerializer,
#         responses={
#             200: HotelAmenityCommonSerializer,
#             400: OpenApiResponse(description="Ошибка валидации"),
#             404: OpenApiResponse(description="Общее удобство в отеле не найдено"),
#         },
#         tags=[tags_hotel_amenity_common_settings["name"]],
#     ),
#     partial_update=extend_schema(
#         summary="Частичное обновление общего удобства в отеле",
#         description="Обновление отдельных полей общего удобства в отеле",
#         request=HotelAmenityCommonSerializer,
#         responses={
#             200: HotelAmenityCommonSerializer,
#             400: OpenApiResponse(description="Ошибка валидации"),
#             404: OpenApiResponse(description="Общее удобство в отеле не найдено"),
#         },
#         tags=[tags_hotel_amenity_common_settings["name"]],
#     ),
#     destroy=extend_schema(
#         summary="Удаление общего удобства в отеле",
#         description="Полное удаление общего удобства в отеле",
#         responses={
#             204: OpenApiResponse(description="Общее удобство в отеле удалено"),
#             404: OpenApiResponse(description="Общее удобство в отеле не найдено"),
#         },
#         tags=[tags_hotel_amenity_common_settings["name"]],
#     ),
# )
# class HotelAmenityCommonViewSet(CreatedByUserFilterMixin, viewsets.ModelViewSet):
#     queryset = HotelAmenityCommon.objects.all()
#     serializer_class = HotelAmenityCommonSerializer
#     pagination_class = None
#
#
# @extend_schema_view(
#     list=extend_schema(
#         summary="Список удобств номера в отеле",
#         description="Получение списка всех удобств номера в отеле",
#         responses={
#             200: HotelAmenityRoomSerializer(many=True),
#             400: OpenApiResponse(description="Ошибка запроса"),
#         },
#         tags=[tags_hotel_amenity_room_settings["name"]],
#     ),
#     create=extend_schema(
#         summary="Добавление удобства номера в отеле",
#         description="Создание нового удобства номера в отеле",
#         request=HotelAmenityRoomSerializer,
#         responses={
#             201: HotelAmenityRoomSerializer,
#             400: OpenApiResponse(description="Ошибка валидации"),
#         },
#         tags=[tags_hotel_amenity_room_settings["name"]],
#     ),
#     retrieve=extend_schema(
#         summary="Детали удобства номера в отеле",
#         description="Получение полной информации удобств номера в отеле",
#         responses={
#             200: HotelAmenityRoomSerializer,
#             404: OpenApiResponse(description="Удобство номера в отеле не найдено"),
#         },
#         tags=[tags_hotel_amenity_room_settings["name"]],
#     ),
#     update=extend_schema(
#         summary="Полное обновление удобств номера в отеле",
#         description="Обновление всех полей удобств номера в отеле",
#         request=HotelAmenityRoomSerializer,
#         responses={
#             200: HotelAmenityRoomSerializer,
#             400: OpenApiResponse(description="Ошибка валидации"),
#             404: OpenApiResponse(description="Удобство номера в отеле не найдено"),
#         },
#         tags=[tags_hotel_amenity_room_settings["name"]],
#     ),
#     partial_update=extend_schema(
#         summary="Частичное обновление удобств номера в отеле",
#         description="Обновление отдельных полей удобств номера в отеле",
#         request=HotelAmenityRoomSerializer,
#         responses={
#             200: HotelAmenityRoomSerializer,
#             400: OpenApiResponse(description="Ошибка валидации"),
#             404: OpenApiResponse(description="Удобство номера в отеле не найдено"),
#         },
#         tags=[tags_hotel_amenity_room_settings["name"]],
#     ),
#     destroy=extend_schema(
#         summary="Удаление удобств номера в отеле",
#         description="Полное удаление удобств номера в отеле",
#         responses={
#             204: OpenApiResponse(description="Удобство номера в отеле удалено"),
#             404: OpenApiResponse(description="Удобство номера в отеле не найдено"),
#         },
#         tags=[tags_hotel_amenity_room_settings["name"]],
#     ),
# )
# class HotelAmenityInTheRoomViewSet(CreatedByUserFilterMixin, viewsets.ModelViewSet):
#     queryset = HotelAmenityInTheRoom.objects.all()
#     serializer_class = HotelAmenityRoomSerializer
#     pagination_class = None
#
#
# @extend_schema_view(
#     list=extend_schema(
#         summary="Список удобств спорта и отдыха в отеле",
#         description="Получение списка всех удобств спорта и отдыха в отеле",
#         responses={
#             200: HotelAmenitySportsSerializer(many=True),
#             400: OpenApiResponse(description="Ошибка запроса"),
#         },
#         tags=[tags_hotel_amenity_sport_settings["name"]],
#     ),
#     create=extend_schema(
#         summary="Добавление удобства спорт и отдых в отеле",
#         description="Создание нового удобства спорт и отдых в отеле",
#         request=HotelAmenitySportsSerializer,
#         responses={
#             201: HotelAmenitySportsSerializer,
#             400: OpenApiResponse(description="Ошибка валидации"),
#         },
#         tags=[tags_hotel_amenity_sport_settings["name"]],
#     ),
#     retrieve=extend_schema(
#         summary="Детали удобства спорт и отдых в отеле",
#         description="Получение полной информации удобств спорт и отдых в отеле",
#         responses={
#             200: HotelAmenitySportsSerializer,
#             404: OpenApiResponse(
#                 description="Удобство спорт и отдых в отеле не найдено"
#             ),
#         },
#         tags=[tags_hotel_amenity_sport_settings["name"]],
#     ),
#     update=extend_schema(
#         summary="Полное обновление удобств спорт и отдых в отеле",
#         description="Обновление всех полей удобств спорт и отдых в отеле",
#         request=HotelAmenitySportsSerializer,
#         responses={
#             200: HotelAmenitySportsSerializer,
#             400: OpenApiResponse(description="Ошибка валидации"),
#             404: OpenApiResponse(
#                 description="Удобство спорт и отдых в отеле не найдено"
#             ),
#         },
#         tags=[tags_hotel_amenity_sport_settings["name"]],
#     ),
#     partial_update=extend_schema(
#         summary="Частичное обновление удобств спорт и отдых в отеле",
#         description="Обновление отдельных полей удобств спорт и отдых в отеле",
#         request=HotelAmenitySportsSerializer,
#         responses={
#             200: HotelAmenitySportsSerializer,
#             400: OpenApiResponse(description="Ошибка валидации"),
#             404: OpenApiResponse(
#                 description="Удобство спорт и отдых в отеле не найдено"
#             ),
#         },
#         tags=[tags_hotel_amenity_sport_settings["name"]],
#     ),
#     destroy=extend_schema(
#         summary="Удаление удобств спорт и отдых в отеле",
#         description="Полное удаление удобств спорт и отдых в отеле",
#         responses={
#             204: OpenApiResponse(description="Удобство спорт и отдых в отеле удалено"),
#             404: OpenApiResponse(
#                 description="Удобство спорт и отдых в отеле не найдено"
#             ),
#         },
#         tags=[tags_hotel_amenity_sport_settings["name"]],
#     ),
# )
# class HotelAmenitySportsAndRecreationViewSet(
#     CreatedByUserFilterMixin, viewsets.ModelViewSet
# ):
#     queryset = HotelAmenitySportsAndRecreation.objects.all()
#     serializer_class = HotelAmenitySportsSerializer
#     pagination_class = None
#
#
# @extend_schema_view(
#     list=extend_schema(
#         summary="Список удобств для детей в отеле",
#         description="Получение списка всех удобств для детей в отеле",
#         responses={
#             200: HotelAmenitySportsSerializer(many=True),
#             400: OpenApiResponse(description="Ошибка запроса"),
#         },
#         tags=[tags_hotel_amenity_children_settings["name"]],
#     ),
#     create=extend_schema(
#         summary="Добавление удобства для детей в отеле",
#         description="Создание нового удобства для детей в отеле",
#         request=HotelAmenitySportsSerializer,
#         responses={
#             201: HotelAmenitySportsSerializer,
#             400: OpenApiResponse(description="Ошибка валидации"),
#         },
#         tags=[tags_hotel_amenity_children_settings["name"]],
#     ),
#     retrieve=extend_schema(
#         summary="Детали удобства для детей в отеле",
#         description="Получение полной информации удобств для детей в отеле",
#         responses={
#             200: HotelAmenitySportsSerializer,
#             404: OpenApiResponse(description="Удобство для детей в отеле не найдено"),
#         },
#         tags=[tags_hotel_amenity_children_settings["name"]],
#     ),
#     update=extend_schema(
#         summary="Полное обновление удобств для детей в отеле",
#         description="Обновление всех полей удобств для детей в отеле",
#         request=HotelAmenitySportsSerializer,
#         responses={
#             200: HotelAmenitySportsSerializer,
#             400: OpenApiResponse(description="Ошибка валидации"),
#             404: OpenApiResponse(description="Удобство для детей в отеле не найдено"),
#         },
#         tags=[tags_hotel_amenity_common_settings["name"]],
#     ),
#     partial_update=extend_schema(
#         summary="Частичное обновление удобств для детей в отеле",
#         description="Обновление отдельных полей удобств для детей в отеле",
#         request=HotelAmenitySportsSerializer,
#         responses={
#             200: HotelAmenitySportsSerializer,
#             400: OpenApiResponse(description="Ошибка валидации"),
#             404: OpenApiResponse(description="Удобство для детей в отеле не найдено"),
#         },
#         tags=[tags_hotel_amenity_children_settings["name"]],
#     ),
#     destroy=extend_schema(
#         summary="Удаление удобств для детей в отеле",
#         description="Полное удаление удобств для детей в отеле",
#         responses={
#             204: OpenApiResponse(description="Удобство для детей в отеле удалено"),
#             404: OpenApiResponse(description="Удобство для детей в отеле не найдено"),
#         },
#         tags=[tags_hotel_amenity_children_settings["name"]],
#     ),
# )
# class HotelAmenityForChildrenViewSet(CreatedByUserFilterMixin, viewsets.ModelViewSet):
#     queryset = HotelAmenityForChildren.objects.all()
#     serializer_class = HotelAmenityChildrenSerializer
#     pagination_class = None
