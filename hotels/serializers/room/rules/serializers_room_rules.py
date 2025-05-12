from rest_framework import serializers

from hotels.models.room.rules.models_room_rules import RoomRules


class RoomRulesSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoomRules
        fields = ("id", "name", "option", "created_by")
        created_by = "created_by"
