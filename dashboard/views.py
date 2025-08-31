from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.models import User
from .forms import PortfolioForm, RegisterForm, AboutForm, SkillsForm, QualificationsForm, ServicesForm, TestimonialsForm
from .models import Portfolio, About, Skill, Qualification, Service, Testimonial
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.forms.models import model_to_dict


from dotenv import load_dotenv
# Create your views here.import os


import os

load_dotenv()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username or len(username) < 3:
            raise forms.ValidationError("Le nom d'utilisateur doit contenir au moins 3 caractères.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email or '@' not in email:
            raise forms.ValidationError("Veuillez entrer une adresse email valide.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and len(password1) < 6:
            self.add_error('password1', "Le mot de passe doit contenir au moins 6 caractères.")
        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Les mots de passe ne correspondent pas.")
        return cleaned_data

@csrf_exempt
def api_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt
def api_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Stateless: do NOT call login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': {'__all__': ['Nom d’utilisateur ou mot de passe incorrect.']}}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt
def api_about(request):
    if request.method == 'POST':
        form = AboutForm(request.POST, request.FILES)
        if form.is_valid():
            about = form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    elif request.method == 'GET':
        abouts = About.objects.all().order_by('-created_at')
        data = []
        for a in abouts:
            d = model_to_dict(a)
            if a.photo:
                d['photo'] = request.build_absolute_uri(a.photo.url)
            if a.cv:
                d['cv'] = request.build_absolute_uri(a.cv.url)
            data.append(d)
        return JsonResponse({'success': True, 'data': data})
    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt
def api_portfolio(request):
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    elif request.method == 'GET':
        portfolios = Portfolio.objects.all().order_by('-created_at')
        data = []
        for p in portfolios:
            d = model_to_dict(p)
            if p.image:
                d['image'] = request.build_absolute_uri(p.image.url)
                #d['image'] = p.image.url
            data.append(d)
        return JsonResponse({'success': True, 'data': data})
    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt
def api_skills(request):
    if request.method == 'POST':
        form = SkillsForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    elif request.method == 'GET':
        skills = Skill.objects.all().order_by('-created_at')
        data = [model_to_dict(s) for s in skills]
        return JsonResponse({'success': True, 'data': data})
    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt
def api_qualifications(request):
    if request.method == 'POST':
        form = QualificationsForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    elif request.method == 'GET':
        qualifications = Qualification.objects.all().order_by('-created_at')
        data = [model_to_dict(q) for q in qualifications]
        return JsonResponse({'success': True, 'data': data})
    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt
def api_services(request):
    if request.method == 'POST':
        form = ServicesForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    elif request.method == 'GET':
        services = Service.objects.all().order_by('-created_at')
        data = [model_to_dict(s) for s in services]
        return JsonResponse({'success': True, 'data': data})
    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt
def api_testimonials(request):
    if request.method == 'POST':
        form = TestimonialsForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    elif request.method == 'GET':
        testimonials = Testimonial.objects.all().order_by('-created_at')
        data = [model_to_dict(t) for t in testimonials]
        return JsonResponse({'success': True, 'data': data})
    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt
def api_edit_about(request, about_id):
    try:
        about = About.objects.get(id=about_id)
        if request.method == 'PUT':
            # Handle both JSON and FormData for PUT requests
            if request.content_type and 'multipart/form-data' in request.content_type:
                # FormData (for file uploads)
                form = AboutForm(request.POST, request.FILES, instance=about)
            else:
                # JSON data
                import json
                data = json.loads(request.body)
                form = AboutForm(data, request.FILES, instance=about)
            
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        elif request.method == 'GET':
            data = model_to_dict(about)
            if about.photo:
                data['photo'] = request.build_absolute_uri(about.photo.url)
            if about.cv:
                data['cv'] = request.build_absolute_uri(about.cv.url)
            return JsonResponse({'success': True, 'data': data})
    except About.DoesNotExist:
        return JsonResponse({'error': 'About not found'}, status=404)

@csrf_exempt
def api_edit_skills(request, skill_id):
    try:
        skill = Skill.objects.get(id=skill_id)
        if request.method == 'PUT':
            import json
            data = json.loads(request.body)
            form = SkillsForm(data, instance=skill)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        elif request.method == 'GET':
            data = model_to_dict(skill)
            return JsonResponse({'success': True, 'data': data})
    except Skill.DoesNotExist:
        return JsonResponse({'error': 'Skill not found'}, status=404)

@csrf_exempt
def api_edit_services(request, service_id):
    try:
        service = Service.objects.get(id=service_id)
        if request.method == 'PUT':
            import json
            data = json.loads(request.body)
            form = ServicesForm(data, instance=service)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        elif request.method == 'GET':
            data = model_to_dict(service)
            return JsonResponse({'success': True, 'data': data})
    except Service.DoesNotExist:
        return JsonResponse({'error': 'Service not found'}, status=404)

@csrf_exempt
def api_edit_portfolio(request, portfolio_id):
    try:
        portfolio = Portfolio.objects.get(id=portfolio_id)
        if request.method == 'PUT':
            # Handle both JSON and FormData for PUT requests
            if request.content_type and 'multipart/form-data' in request.content_type:
                # FormData (for file uploads)
                form = PortfolioForm(request.POST, request.FILES, instance=portfolio)
            else:
                # JSON data
                import json
                data = json.loads(request.body)
                form = PortfolioForm(data, request.FILES, instance=portfolio)
            
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        elif request.method == 'GET':
            data = model_to_dict(portfolio)
            if portfolio.image:
                data['image'] = request.build_absolute_uri(portfolio.image.url)
            return JsonResponse({'success': True, 'data': data})
    except Portfolio.DoesNotExist:
        return JsonResponse({'error': 'Portfolio not found'}, status=404)

@csrf_exempt
def api_edit_qualifications(request, qualification_id):
    try:
        qualification = Qualification.objects.get(id=qualification_id)
        if request.method == 'PUT':
            import json
            data = json.loads(request.body)
            form = QualificationsForm(data, instance=qualification)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        elif request.method == 'GET':
            data = model_to_dict(qualification)
            return JsonResponse({'success': True, 'data': data})
    except Qualification.DoesNotExist:
        return JsonResponse({'error': 'Qualification not found'}, status=404)

@csrf_exempt
def api_edit_testimonials(request, testimonial_id):
    try:
        testimonial = Testimonial.objects.get(id=testimonial_id)
        if request.method == 'PUT':
            import json
            data = json.loads(request.body)
            form = TestimonialsForm(data, instance=testimonial)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        elif request.method == 'GET':
            data = model_to_dict(testimonial)
            return JsonResponse({'success': True, 'data': data})
    except Testimonial.DoesNotExist:
        return JsonResponse({'error': 'Testimonial not found'}, status=404)

def logout_view(request):
    logout(request)
    return redirect('login')

#@login_required
def dashboard_home(request):
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard_home')
    else:
        form = PortfolioForm()
    portfolios = Portfolio.objects.all().order_by('-created_at')
    return render(request, 'dashboard_home.html', {'form': form, 'portfolios': portfolios})

def public_index(request):
    portfolios = Portfolio.objects.all().order_by('-created_at')
    return render(request, 'public_index.html', {'portfolios': portfolios})

def login_view(request):
    return render(request, 'login.html')

def register_view(request):
    
    return render(request, 'register.html')

def about_view(request):
    context={
        "base_url": os.getenv("base_url")
    }
    return render(request, 'about.html', context)

def skills_view(request):
    context={
        "base_url": os.getenv("base_url")
    }
    return render(request, 'skills.html', context)

def services_view(request):
    context={
        "base_url": os.getenv("base_url")
    }
    return render(request, 'services.html', context)

def portfolio_view(request):
    context={
        "base_url": os.getenv("base_url")
    }
    return render(request, 'portfolio.html', context)

def qualifications_view(request):
    context={
        "base_url": os.getenv("base_url")
    }
    return render(request, 'qualifications.html', context)

def testimonials_view(request):
    context={
        "base_url": os.getenv("base_url")
    }
    return render(request, 'testimonials.html', context)

def dashboard_view(request):
    context={
        "base_url": os.getenv("base_url")
    }
    return render(request, 'dashboard.html', context)

def index_view(request):
    context={
        "base_url": os.getenv("base_url")
    }
    return render(request, 'index.html', context)

def edit_about_view(request, about_id):
    return render(request, 'about.html', {'is_edit': True, 'item_id': about_id})

def edit_skills_view(request, skill_id):
    return render(request, 'skills.html', {'is_edit': True, 'item_id': skill_id})

def edit_services_view(request, service_id):
    return render(request, 'services.html', {'is_edit': True, 'item_id': service_id})

def edit_portfolio_view(request, portfolio_id):
    return render(request, 'portfolio.html', {'is_edit': True, 'item_id': portfolio_id})

def edit_qualifications_view(request, qualification_id):
    return render(request, 'qualifications.html', {'is_edit': True, 'item_id': qualification_id})

def edit_testimonials_view(request, testimonial_id):
    return render(request, 'testimonials.html', {'is_edit': True, 'item_id': testimonial_id})
