from time import sleep
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from tickets.models import Ticket, Message
from tickets.permissions import IsOwner, RoleIsAdmin, RoleIsManager, RoleIsUser
from tickets.serializers import (
    MessageSerializer,
    TicketAssignSerializer,
    TicketSerializer,
)
from tickets.services import AssignService
from users.constants import Role

User = get_user_model()


# def scheduler(id: int, func: Callable, *args, **kwargs):
#     t = threading.Thread(name=id, target = func, *args, **kwargs)
#     t.start(daemon=True)

# class SchedulerStatus(StrEnum):
#     NOT_STARTED = auto()
#     STARTED = auto()
#     COMPLETED = auto()
#     FAILED = auto()


# @dataclass
# class SchedulerResponse:
#     status: SchedulerStatus
#     data: Any


class TicketAPIViewSet(ModelViewSet):
    serializer_class = TicketSerializer

    def get_queryset(self):
        user = self.request.user
        all_tickets = Ticket.objects.all()

        sleep(15)

        if user.role == Role.ADMIN:
            return all_tickets
        elif user.role == Role.MANAGER:
            return all_tickets.filter(Q(manager=user) | Q(manager=None))
        else:
            # User's role fallback solution
            return all_tickets.filter(user=user)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == "list":
            permission_classes = [RoleIsAdmin | RoleIsManager | RoleIsUser]
        elif self.action == "create":
            permission_classes = [RoleIsUser]
        elif self.action == "retrieve":
            permission_classes = [IsOwner | RoleIsAdmin | RoleIsManager]
        elif self.action == "update":
            permission_classes = [RoleIsAdmin | RoleIsManager]
        elif self.action == "destroy":
            permission_classes = [RoleIsAdmin | RoleIsManager]
        elif self.action == "take":
            permission_classes = [RoleIsManager]
        else:
            permission_classes = []

        return [permission() for permission in permission_classes]

    @action(detail=True, methods=["post"])
    def take(self, request, pk):
        ticket = self.get_object()

        # *****************************************************
        # Custom services approach
        # *****************************************************
        # updated_ticket: Ticket = AssignService(ticket).assign_manager(
        #     request.user,
        # )
        # serializer = self.get_serializer(ticket)

        # *****************************************************
        # Serializers approach
        # *****************************************************
        serializer = TicketAssignSerializer(data={"manager_id": request.user.id})
        serializer.is_valid()
        ticket = serializer.assign(ticket)

        return Response(TicketSerializer(ticket).data)

    @action(detail=True, methods=["post"])
    def reassign(self, request, pk):
        ticket = self.get_object()
        serializer = TicketAssignSerializer(data={"manager_id": request.user.id})
        serializer.is_valid()
        ticket = serializer.assign(ticket)

        return Response(TicketSerializer(ticket).data)


class MessageListCreateAPIView(ListCreateAPIView):
    serializer_class = MessageSerializer
    lookup_field = "ticket_id"

    def get_queryset(self):
        # ticket = get_object_or_404(
        #     Ticket.objects.all(), id=self.kwargs[self.lookup_field]
        # )
        # if ticket.user != self.request.user and ticket.manager != self.request.user:
        #     raise Http404

        return Message.objects.filter(
            Q(ticket__user=self.request.user) | Q(ticket__manager=self.request.user),
            ticket_id=self.kwargs[self.lookup_field],
        )

    @staticmethod
    def get_ticket(user: User, ticket_id: int) -> Ticket:
        """Get tickets for current user."""

        tickets = Ticket.objects.filter(Q(user=user) | Q(manager=user))
        return get_object_or_404(tickets, id=ticket_id)

    def post(self, request, ticket_id: int):
        ticket = self.get_ticket(request.user, ticket_id)
        payload = {
            "text": request.data["text"],
            "ticket": ticket.id,
        }
        serializer = self.get_serializer(data=payload)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
