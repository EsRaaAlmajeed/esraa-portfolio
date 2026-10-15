from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse
from .models import Project, Category

# Create your views here.
def home(request):
    categories = Category.objects.all()
    projects = Project.objects.all()

    category_id = request.GET.get('category')

    if category_id:
        projects = projects.filter(category_id=category_id)

    context = {
        'categories': categories,
        'projects': projects,
        'selected_category': category_id,
    }

    return render(request, 'portfolio/home.html', context)

def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)

    return render(
        request,
        'portfolio/project_detail.html',
        {'project': project}
    )