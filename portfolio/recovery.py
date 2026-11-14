
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
        <head><title>Admin Password Recovery</title></head>
        <body>
            <h2>Admin Password Recovery</h2>
            <p>{escape(message)}</p>
            <form method="POST">
                <input type="hidden" name="csrfmiddlewaretoken"
                       value="{escape(csrf_token)}">

                <label>Recovery Key:</label><br>
                <input type="password" name="recovery_key" required><br><br>

                <label>Username:</label><br>
                <input type="text" name="username" required><br><br>

                <label>New Password:</label><br>
                <input type="password" name="new_password"
                       autocomplete="new-password" required><br><br>

                <button type="submit">Reset Password</button>
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

    username = request.POST.get("username", "")
    new_password = request.POST.get("new_password", "")

    User = get_user_model()
    user = User.objects.filter(
        username=username,
        is_superuser=True
    ).first()

    if not user:
        return recovery_page(request, "Invalid username.")

    try:
        validate_password(new_password, user)
    except ValidationError as error:
        return recovery_page(request, " ".join(error.messages))

    user.set_password(new_password)
    user.save()

    return HttpResponse(
        "Password changed successfully. You can now log in to Django Admin.",
        headers={"Cache-Control": "no-store"}
    )
