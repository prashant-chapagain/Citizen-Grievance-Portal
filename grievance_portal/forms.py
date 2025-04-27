from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Grievance, GrievanceResponse, UserProfile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone = forms.CharField(max_length=15, required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                phone=self.cleaned_data['phone'],
                address=self.cleaned_data['address']
            )
        
        return user

class GrievanceForm(forms.ModelForm):
    class Meta:
        model = Grievance
        fields = ('title', 'description', 'category', 'attachment')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }

class GrievanceResponseForm(forms.ModelForm):
    class Meta:
        model = GrievanceResponse
        fields = ('response',)
        widgets = {
            'response': forms.Textarea(attrs={'rows': 3}),
        }

class GrievanceStatusForm(forms.ModelForm):
    class Meta:
        model = Grievance
        fields = ('status',)