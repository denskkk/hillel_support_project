from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
# fmt: off
from tickets.models import Message, Ticket
from tickets.permissions import IsOwner, RoleIsAdmin, RoleIsManager, RoleIsUser
from tickets.serializers import (MessageSerializer, TicketAssignSerializer,
                                 TicketSerializer)
from users.constants import Role
# fmt: on
User = get_user_model()


class TicketAPIViewSet(ModelViewSet):
    serializer_class = TicketSerializer

    def get_queryset(self):
        user = self.request.user
        all_tickets = Ticket.objects.all()

        if user.role == Role.ADMIN:
            return all_tickets
        elif user.role == Role.MANAGER:
            return all_tickets.filter(Q(manager=user) | Q(manager=None))
        else:
            # User's role fallback solution
            return all_tickets.filter(user=user)

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [RoleIsAdmin | RoleIsManager | RoleIsUser]
        elif self.action == "create":
            permission_classes = [RoleIsUser]
        elif self.action == "retrieve":
            permission_classes = [IsOwner | RoleIsAdmin | RoleIsManager]
        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [RoleIsAdmin | RoleIsManager]
        elif self.action == "take":
            permission_classes = [RoleIsManager]
        elif self.action == "reassign":
            permission_classes = [RoleIsAdmin]
        else:
            permission_classes = []

        return [permission() for permission in permission_classes]

    @action(detail=True, methods=["post"])
    def take(self, request, pk):
        ticket = self.get_object()

        serializer = TicketAssignSerializer(
            data={"manager_id": request.user.id}
        )  # noqa
        serializer.is_valid()
        ticket = serializer.assign(ticket)

        return Response(TicketSerializer(ticket).data)

    @action(detail=True, methods=["put"])
    def reassign(self, request, pk):
        ticket = self.get_object()

        if ticket.manager_id == request.data.get("new_manager"):
            return Response(
                {
                    "detail": "The new manager is the same as the current manager."  # noqa
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = TicketAssignSerializer(
            data={"manager_id": request.data.get("new_manager")}
        )  # noqa
        serializer.is_valid(raise_exception=True)
        ticket = serializer.assign(ticket)

        return Response(TicketSerializer(ticket).data)


class MessageListCreateAPIView(ListCreateAPIView):
    serializer_class = MessageSerializer
    lookup_field = "ticket_id"

    def get_queryset(self):
        return Message.objects.filter(
            Q(ticket__user=self.request.user)
            | Q(ticket__manager=self.request.user),  # noqa
            ticket_id=self.kwargs[self.lookup_field],
        )

    @staticmethod
    def get_ticket(user: User, ticket_id: int) -> Ticket:
        tickets = Ticket.objects.filter(Q(user=user) | Q(manager=user))
        return get_object_or_404(tickets, id=ticket_id)

    def post(self, request, ticket_id: int):
        ticket = self.get_ticket(request.user, ticket_id)
        payload = {
            "text": request.data["text"],
            "user": request.user.id,
            "ticket": ticket.id,
        }
        serializer = self.get_serializer(data=payload)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
