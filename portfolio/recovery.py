
import os
import secrets
from html import escape

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods


def recovery_page(request, message=""):
    csrf_token = get_token(request)

    return HttpResponse(f"""
        <!DOCTYPE html>
        <html>
        <head><title>Admin Account Recovery</title></head>
        <body>
            <h2>Create Admin Account</h2>
            <p>{escape(message)}</p>

            <form method="POST">
                <input type="hidden" name="csrfmiddlewaretoken"
                       value="{escape(csrf_token)}">

                <label>Recovery Key:</label><br>
                <input type="password" name="recovery_key" required><br><br>

                <label>Username:</label><br>
                <input type="text" name="username" required><br><br>

                <label>Email:</label><br>
                <input type="email" name="email" required><br><br>

                <label>New Password:</label><br>
                <input type="password" name="new_password"
                       autocomplete="new-password" required><br><br>

                <button type="submit">Create Admin Account</button>
            </form>
        </body>
        </html>
    """, headers={"Cache-Control": "no-store"})


@csrf_protect
@require_http_methods(["GET", "POST"])
def reset_admin_password(request):
    recovery_key = os.environ.get("ADMIN_RECOVERY_KEY")

    if not recovery_key:
        return HttpResponse("Recovery is not configured.", status=503)

    if request.method == "GET":
        return recovery_page(request)

    submitted_key = request.POST.get("recovery_key", "")

    if not secrets.compare_digest(submitted_key, recovery_key):
        return recovery_page(request, "Invalid recovery key.")

    User = get_user_model()

    if User.objects.filter(is_superuser=True).exists():
        return HttpResponse(
            "An administrator account already exists. Recovery stopped."
        )

    username = request.POST.get("username", "").strip()
    email = request.POST.get("email", "").strip()
    password = request.POST.get("new_password", "")

    if not username or not email or not password:
        return recovery_page(request, "All fields are required.")

    if User.objects.filter(username=username).exists():
        return recovery_page(request, "Username already exists.")

    user = User(username=username, email=email)

    try:
        validate_password(password, user)
    except ValidationError as error:
        return recovery_page(request, " ".join(error.messages))

    User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )

    return HttpResponse(
        "Admin account created successfully. You can now log in.",
        headers={"Cache-Control": "no-store"}
    )
