
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


def recovery_page(request, message="", users=None):
    csrf_token = get_token(request)

    account_field = ""

    if users is not None:
        options = "".join(
            f'<option value="{user.pk}">'
            f'{escape(str(user.get_username()))}</option>'
            for user in users
        )

        account_field = f"""
            <label>Select Admin Account:</label><br>
            <select name="account_id" required>
                <option value="">Choose an account</option>
                {options}
            </select><br><br>
        """

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

                {account_field}

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

    User = get_user_model()

    users = list(
        User.objects.filter(is_superuser=True, is_active=True)
    )

    if not users:
        return HttpResponse("No active administrator account found.")

    account_id = request.POST.get("account_id", "")

    if not account_id:
        if len(users) == 1:
            user = users[0]
        else:
            return recovery_page(
                request,
                "Select the administrator account.",
                users
            )
    else:
        user = next(
            (u for u in users if str(u.pk) == account_id),
            None
        )

        if user is None:
            return recovery_page(request, "Invalid account selection.")

    new_password = request.POST.get("new_password", "")

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
