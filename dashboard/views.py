from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.models import User
from .forms import PortfolioForm, RegisterForm, AboutForm, SkillsForm, QualificationsForm, ServicesForm, TestimonialsForm
from .models import Portfolio, About, Skill, Qualification, Service, Testimonial, UserProfile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.forms.models import model_to_dict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from functools import wraps

import json


from dotenv import load_dotenv
# Create your views here.import os


import os

load_dotenv()

def csrf_exempt_and_login_required(view_func):
    """
    Custom decorator that combines csrf_exempt with login_required
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        return view_func(request, *args, **kwargs)
    return csrf_exempt(wrapper)



@csrf_exempt
def api_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create UserProfile
            UserProfile.objects.create(
                user=user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email']
            )
            # Don't auto-login, redirect to login page
            return JsonResponse({'success': True, 'redirect_url': '/login/'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt
def api_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Try to find user by email
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'success': True, 'redirect_url': '/dashboard/'})
            else:
                return JsonResponse({'success': False, 'errors': {'__all__': ['Email ou mot de passe incorrect.']}}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'errors': {'__all__': ['Email ou mot de passe incorrect.']}}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt_and_login_required
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

@csrf_exempt_and_login_required
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

@csrf_exempt_and_login_required
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

@csrf_exempt_and_login_required
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

@csrf_exempt_and_login_required
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

@csrf_exempt_and_login_required
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

@csrf_exempt_and_login_required
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

@csrf_exempt_and_login_required
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

@csrf_exempt_and_login_required
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

@csrf_exempt_and_login_required
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

@csrf_exempt_and_login_required
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

@csrf_exempt_and_login_required
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
    context = {
        "base_url": request.build_absolute_uri('/').rstrip('/')
    }
    return render(request, 'login.html', context)

def register_view(request):
    context = {
        "base_url": request.build_absolute_uri('/').rstrip('/')
    }
    return render(request, 'register.html', context)

@login_required
def about_view(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None
    
    context={
        "base_url": request.build_absolute_uri('/').rstrip('/'),
        "user": request.user,
        "user_profile": user_profile
    }
    return render(request, 'about.html', context)

@login_required
def skills_view(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None
    
    context={
        "base_url": request.build_absolute_uri('/').rstrip('/'),
        "user": request.user,
        "user_profile": user_profile
    }
    return render(request, 'skills.html', context)

@login_required
def services_view(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None
    
    context={
        "base_url": request.build_absolute_uri('/').rstrip('/'),
        "user": request.user,
        "user_profile": user_profile
    }
    return render(request, 'services.html', context)

@login_required
def portfolio_view(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None
    
    context={
        "base_url": request.build_absolute_uri('/').rstrip('/'),
        "user": request.user,
        "user_profile": user_profile
    }
    return render(request, 'portfolio.html', context)

@login_required
def qualifications_view(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None
    
    context={
        "base_url": request.build_absolute_uri('/').rstrip('/'),
        "user": request.user,
        "user_profile": user_profile
    }
    return render(request, 'qualifications.html', context)

@login_required
def testimonials_view(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None
    
    context={
        "base_url": request.build_absolute_uri('/').rstrip('/'),
        "user": request.user,
        "user_profile": user_profile
    }
    return render(request, 'testimonials.html', context)

@login_required
def dashboard_view(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None
    
    context={
        "base_url": request.build_absolute_uri('/').rstrip('/'),
        "user": request.user,
        "user_profile": user_profile
    }
    return render(request, 'dashboard.html', context)

@login_required
def index_view(request, user_id=None):
    # If user_id is provided, verify it matches the logged-in user
    if user_id and user_id != request.user.id:
        return redirect('index', user_id=request.user.id)
    
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None
    
    context={
        "base_url": request.build_absolute_uri('/').rstrip('/'),
        "user": request.user,
        "user_profile": user_profile
    }
    return render(request, 'index.html', context)

@login_required
def edit_about_view(request, about_id):
    return render(request, 'about.html', {'is_edit': True, 'item_id': about_id, 'user': request.user})

@login_required
def edit_skills_view(request, skill_id):
    return render(request, 'skills.html', {'is_edit': True, 'item_id': skill_id, 'user': request.user})

@login_required
def edit_services_view(request, service_id):
    return render(request, 'services.html', {'is_edit': True, 'item_id': service_id, 'user': request.user})

@login_required
def edit_portfolio_view(request, portfolio_id):
    return render(request, 'portfolio.html', {'is_edit': True, 'item_id': portfolio_id, 'user': request.user})

@login_required
def edit_qualifications_view(request, qualification_id):
    return render(request, 'qualifications.html', {'is_edit': True, 'item_id': qualification_id, 'user': request.user})

@login_required
def edit_testimonials_view(request, testimonial_id):
    return render(request, 'testimonials.html', {'is_edit': True, 'item_id': testimonial_id, 'user': request.user})

# Delete API endpoints
@csrf_exempt_and_login_required
def api_delete_about(request, about_id):
    if request.method == 'DELETE':
        try:
            about = get_object_or_404(About, id=about_id)
            about.delete()
            return JsonResponse({'success': True, 'message': 'Profil supprimé avec succès'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt_and_login_required
def api_delete_skill(request, skill_id):
    if request.method == 'DELETE':
        try:
            skill = get_object_or_404(Skill, id=skill_id)
            skill.delete()
            return JsonResponse({'success': True, 'message': 'Compétence supprimée avec succès'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt_and_login_required
def api_delete_qualification(request, qualification_id):
    if request.method == 'DELETE':
        try:
            qualification = get_object_or_404(Qualification, id=qualification_id)
            qualification.delete()
            return JsonResponse({'success': True, 'message': 'Qualification supprimée avec succès'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt_and_login_required
def api_delete_service(request, service_id):
    if request.method == 'DELETE':
        try:
            service = get_object_or_404(Service, id=service_id)
            service.delete()
            return JsonResponse({'success': True, 'message': 'Service supprimé avec succès'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt_and_login_required
def api_delete_portfolio(request, portfolio_id):
    if request.method == 'DELETE':
        try:
            portfolio = get_object_or_404(Portfolio, id=portfolio_id)
            portfolio.delete()
            return JsonResponse({'success': True, 'message': 'Projet supprimé avec succès'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt_and_login_required
def api_delete_testimonial(request, testimonial_id):
    if request.method == 'DELETE':
        try:
            testimonial = get_object_or_404(Testimonial, id=testimonial_id)
            testimonial.delete()
            return JsonResponse({'success': True, 'message': 'Témoignage supprimé avec succès'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)



# -------------------- ABOUT --------------------
@csrf_exempt_and_login_required
def api_edit_delete_about(request, about_id):
    try:
        about = About.objects.get(id=about_id)

        if request.method == 'PUT':
            if request.content_type and 'multipart/form-data' in request.content_type:
                form = AboutForm(request.POST, request.FILES, instance=about)
            else:
                data = json.loads(request.body)
                form = AboutForm(data, request.FILES, instance=about)

            if form.is_valid():
                form.save()
                return JsonResponse({'success': True})
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

        elif request.method == 'GET':
            data = model_to_dict(about)
            if about.photo:
                data['photo'] = request.build_absolute_uri(about.photo.url)
            if about.cv:
                data['cv'] = request.build_absolute_uri(about.cv.url)
            return JsonResponse({'success': True, 'data': data})

        elif request.method == 'DELETE':
            about.delete()
            return JsonResponse({'success': True, 'message': 'About deleted successfully'})

        return JsonResponse({'error': 'Method not allowed'}, status=405)

    except About.DoesNotExist:
        return JsonResponse({'error': 'About not found'}, status=404)


# -------------------- SKILLS --------------------
@csrf_exempt_and_login_required
def api_edit_delete_skills(request, skill_id):
    try:
        skill = Skill.objects.get(id=skill_id)

        if request.method == 'PUT':
            data = json.loads(request.body)
            form = SkillsForm(data, instance=skill)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True})
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

        elif request.method == 'GET':
            data = model_to_dict(skill)
            return JsonResponse({'success': True, 'data': data})

        elif request.method == 'DELETE':
            skill.delete()
            return JsonResponse({'success': True, 'message': 'Skill deleted successfully'})

        return JsonResponse({'error': 'Method not allowed'}, status=405)

    except Skill.DoesNotExist:
        return JsonResponse({'error': 'Skill not found'}, status=404)


# -------------------- SERVICES --------------------
@csrf_exempt_and_login_required
def api_edit_delete_services(request, service_id):
    try:
        service = Service.objects.get(id=service_id)

        if request.method == 'PUT':
            data = json.loads(request.body)
            form = ServicesForm(data, instance=service)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True})
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

        elif request.method == 'GET':
            data = model_to_dict(service)
            return JsonResponse({'success': True, 'data': data})

        elif request.method == 'DELETE':
            service.delete()
            return JsonResponse({'success': True, 'message': 'Service deleted successfully'})

        return JsonResponse({'error': 'Method not allowed'}, status=405)

    except Service.DoesNotExist:
        return JsonResponse({'error': 'Service not found'}, status=404)


# -------------------- PORTFOLIO --------------------
@csrf_exempt_and_login_required
def api_edit_delete_portfolio(request, portfolio_id):
    try:
        portfolio = Portfolio.objects.get(id=portfolio_id)

        if request.method == 'PUT':
            if request.content_type and 'multipart/form-data' in request.content_type:
                form = PortfolioForm(request.POST, request.FILES, instance=portfolio)
            else:
                data = json.loads(request.body)
                form = PortfolioForm(data, request.FILES, instance=portfolio)

            if form.is_valid():
                form.save()
                return JsonResponse({'success': True})
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

        elif request.method == 'GET':
            data = model_to_dict(portfolio)
            if portfolio.image:
                data['image'] = request.build_absolute_uri(portfolio.image.url)
            return JsonResponse({'success': True, 'data': data})

        elif request.method == 'DELETE':
            portfolio.delete()
            return JsonResponse({'success': True, 'message': 'Portfolio deleted successfully'})

        return JsonResponse({'error': 'Method not allowed'}, status=405)

    except Portfolio.DoesNotExist:
        return JsonResponse({'error': 'Portfolio not found'}, status=404)


# -------------------- QUALIFICATIONS --------------------
@csrf_exempt_and_login_required
def api_edit_delete_qualifications(request, qualification_id):
    try:
        qualification = Qualification.objects.get(id=qualification_id)

        if request.method == 'PUT':
            data = json.loads(request.body)
            form = QualificationsForm(data, instance=qualification)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True})
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

        elif request.method == 'GET':
            data = model_to_dict(qualification)
            return JsonResponse({'success': True, 'data': data})

        elif request.method == 'DELETE':
            qualification.delete()
            return JsonResponse({'success': True, 'message': 'Qualification deleted successfully'})

        return JsonResponse({'error': 'Method not allowed'}, status=405)

    except Qualification.DoesNotExist:
        return JsonResponse({'error': 'Qualification not found'}, status=404)


# -------------------- TESTIMONIALS --------------------
@csrf_exempt_and_login_required
def api_edit_delete_testimonials(request, testimonial_id):
    try:
        testimonial = Testimonial.objects.get(id=testimonial_id)

        if request.method == 'PUT':
            data = json.loads(request.body)
            form = TestimonialsForm(data, instance=testimonial)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True})
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

        elif request.method == 'GET':
            data = model_to_dict(testimonial)
            return JsonResponse({'success': True, 'data': data})

        elif request.method == 'DELETE':
            testimonial.delete()
            return JsonResponse({'success': True, 'message': 'Testimonial deleted successfully'})

        return JsonResponse({'error': 'Method not allowed'}, status=405)

    except Testimonial.DoesNotExist:
        return JsonResponse({'error': 'Testimonial not found'}, status=404)
