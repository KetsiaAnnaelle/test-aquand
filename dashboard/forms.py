from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Portfolio, About, Skill, Qualification, Service, Testimonial

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

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['title', 'url', 'description', 'image']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title or len(title) < 3:
            raise forms.ValidationError("Le titre doit contenir au moins 3 caractères.")
        return title

    def clean_url(self):
        url = self.cleaned_data.get('url')
        if url and not url.startswith('http'):
            raise forms.ValidationError("Le lien doit commencer par http ou https.")
        return url

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description or len(description) < 10:
            raise forms.ValidationError("La description doit contenir au moins 10 caractères.")
        return description

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            raise forms.ValidationError("L'image du projet est requise.")
        return image

class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = ['first_name', 'last_name', 'profession', 'years_experience', 'completed_projects', 
                 'address', 'email', 'phone', 'company_name', 'bio', 'photo', 'cv']
        widgets = {
            'years_experience': forms.NumberInput(attrs={'min': 0}),
            'completed_projects': forms.NumberInput(attrs={'min': 0}),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name or len(first_name) < 2:
            raise forms.ValidationError("Le prénom doit contenir au moins 2 caractères.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name or len(last_name) < 2:
            raise forms.ValidationError("Le nom doit contenir au moins 2 caractères.")
        return last_name

    def clean_profession(self):
        profession = self.cleaned_data.get('profession')
        if not profession or len(profession) < 3:
            raise forms.ValidationError("La profession doit contenir au moins 3 caractères.")
        return profession

    def clean_years_experience(self):
        years = self.cleaned_data.get('years_experience')
        if years is None or years < 0:
            raise forms.ValidationError("Les années d'expérience doivent être un nombre positif.")
        return years

    def clean_completed_projects(self):
        projects = self.cleaned_data.get('completed_projects')
        if projects is None or projects < 0:
            raise forms.ValidationError("Le nombre de projets doit être un nombre positif.")
        return projects

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email or '@' not in email:
            raise forms.ValidationError("Veuillez entrer une adresse email valide.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone or len(phone) < 8:
            raise forms.ValidationError("Le numéro de téléphone doit contenir au moins 8 chiffres.")
        return phone

    def clean_bio(self):
        bio = self.cleaned_data.get('bio')
        if not bio or len(bio) < 10:
            raise forms.ValidationError("La bio doit contenir au moins 10 caractères.")
        return bio

class SkillsForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['skill', 'level', 'years_experience', 'description']
        widgets = {
            'years_experience': forms.NumberInput(attrs={'min': 0}),
        }

    def clean_skill(self):
        skill = self.cleaned_data.get('skill')
        if not skill or len(skill) < 2:
            raise forms.ValidationError("Le nom de la compétence doit contenir au moins 2 caractères.")
        return skill

    def clean_years_experience(self):
        years = self.cleaned_data.get('years_experience')
        if years is None or years < 0:
            raise forms.ValidationError("Les années d'expérience doivent être un nombre positif.")
        return years

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description and len(description) < 10:
            raise forms.ValidationError("La description doit contenir au moins 10 caractères.")
        return description

class QualificationsForm(forms.ModelForm):
    class Meta:
        model = Qualification
        fields = ['type', 'diploma', 'institution', 'year']

    def clean_diploma(self):
        diploma = self.cleaned_data.get('diploma')
        if not diploma or len(diploma) < 3:
            raise forms.ValidationError("Le diplôme doit contenir au moins 3 caractères.")
        return diploma

    def clean_institution(self):
        institution = self.cleaned_data.get('institution')
        if not institution or len(institution) < 3:
            raise forms.ValidationError("L'institution doit contenir au moins 3 caractères.")
        return institution

    def clean_year(self):
        year = self.cleaned_data.get('year')
        if not year or len(year) != 4 or not year.isdigit():
            raise forms.ValidationError("L'année doit être au format YYYY (ex: 2023).")
        return year

class ServicesForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['service', 'description']

class TestimonialsForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['author', 'testimonial'] 