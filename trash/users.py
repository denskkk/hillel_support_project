import hashlib
import json
from core.models import User
from django.http import HttpResponse


def _validate_email(email: str) -> None:
    if "@" not in email or ".com" not in email:
        raise ValueError("Email is not correct")


def _validate_unique(instances: object, payload: dict, *fields: str):
    for field in fields:
        elements = {getattr(instance, field) for instance in instances}
        if payload[field] in elements:
            raise ValueError(f"The {field} already exists.")


def hash_password(payload: str) -> str:
    return hashlib.md5(payload.encode()).hexdigest()


def create_user(request):
    if request.method != "POST":
        raise ValueError("Only post method is allowed")

    if not request.body:
        raise ValueError("Request body is empty")

    data = json.loads(request.body)

    _validate_email(data["email"])

    users = User.objects.all()
    _validate_unique(users, data, "username", "email")
    hashed_password: str = hash_password(data["password"])

    user = User.objects.create(**data)

    result = {
        "id": user.pk,
        "username": user.username,
        "email": user.email,
        "firstName": user.first_name,
        "lastName": user.last_name,
        "role": user.role,
    }

    return HttpResponse(
        content_type="application/json",
        content=json.dumps(result),
    )
