from rest_framework import serializers

from tickets.models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Ticket
        fields = [
            "id",
            "title",
            "text",
            "visibility",
            "status",
            "user",
            "manager",
        ]  # noqa
        read_only_fields = ["visibility", "manager"]


def validate_manager_id(manager_id):
    return manager_id


class TicketAssignSerializer(serializers.Serializer):
    manager_id = serializers.IntegerField()

    def assign(self, ticket: Ticket) -> Ticket:
        ticket.manager_id = self.validated_data["manager_id"]
        ticket.save()

        return ticket
