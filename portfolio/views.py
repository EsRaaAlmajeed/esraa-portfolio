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