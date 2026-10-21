import os
import secrets
from pathlib import Path

from django.core.management import call_command
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse
from .models import Project, Category, Certification

# Create your views here.
def home(request):
    categories = Category.objects.all()
    projects = Project.objects.all()
    certifications = Certification.objects.all().order_by('display_order')


    category_id = request.GET.get('category')

    if category_id:
        projects = projects.filter(category_id=category_id)

    context = {
        'categories': categories,
        'projects': projects,
        'selected_category': category_id,
        'certifications': certifications,
    }

    return render(request, 'portfolio/home.html', context)

def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)

    return render(
        request,
        'portfolio/project_detail.html',
        {'project': project}
    )
@csrf_exempt
def temporary_import(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "POST method required"},
            status=405,
        )

    expected_token = os.environ.get("PORTFOLIO_IMPORT_TOKEN", "")
    received_token = request.headers.get("X-Import-Token", "")

    if not expected_token or not secrets.compare_digest(
        received_token, expected_token
    ):
        return JsonResponse({"error": "Unauthorized"}, status=401)

    fixture_path = Path(__file__).resolve().parent.parent / "portfolio_data.json"

    if not fixture_path.is_file():
        return JsonResponse(
            {"error": "Fixture file not found"},
            status=500,
        )

    try:
        call_command("loaddata", str(fixture_path), verbosity=0)
        return JsonResponse({"message": "Import successful"})
    except Exception:
        return JsonResponse(
            {"error": "Import failed. Check the application logs."},
            status=500,
        )