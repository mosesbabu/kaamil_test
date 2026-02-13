from django import forms
from .models import (
    Application, PersonalDetails, AddressEntry, Premises,
    ChildcareService, Training, EmploymentEntry, HouseholdMember,
    Suitability, Declaration, Reference
)

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status'] # Usually user doesn't set status, but handled in view

class PersonalDetailsForm(forms.ModelForm):
    class Meta:
        model = PersonalDetails
        exclude = ['application']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }

class PremisesForm(forms.ModelForm):
    class Meta:
        model = Premises
        exclude = ['application']
        widgets = {
            'pets_details': forms.Textarea(attrs={'rows': 3}),
        }

class ChildcareServiceForm(forms.ModelForm):
    class Meta:
        model = ChildcareService
        exclude = ['application']

class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        exclude = ['application']
        widgets = {
            'first_aid_date': forms.DateInput(attrs={'type': 'date'}),
            'safeguarding_date': forms.DateInput(attrs={'type': 'date'}),
            'eyfs_date': forms.DateInput(attrs={'type': 'date'}),
            'food_hygiene_date': forms.DateInput(attrs={'type': 'date'}),
        }

class SuitabilityForm(forms.ModelForm):
    class Meta:
        model = Suitability
        exclude = ['application']
        widgets = {
            'medical_condition_details': forms.Textarea(attrs={'rows': 4}),
            'social_services_details': forms.Textarea(attrs={'rows': 4}),
        }

class DeclarationForm(forms.ModelForm):
    class Meta:
        model = Declaration
        exclude = ['application']
        widgets = {
            'date_signed': forms.DateInput(attrs={'type': 'date'}),
        }

# Address History FormSet
AddressEntryFormSet = forms.inlineformset_factory(
    Application, AddressEntry,
    fields=['line1', 'line2', 'town', 'postcode', 'move_in_date', 'is_current'],
    widgets={'move_in_date': forms.DateInput(attrs={'type': 'date'})},
    extra=1,
    can_delete=True
)

# Employment FormSet
EmploymentEntryFormSet = forms.inlineformset_factory(
    Application, EmploymentEntry,
    fields=['employer_name', 'role', 'start_date', 'end_date', 'is_current'],
    widgets={
        'start_date': forms.DateInput(attrs={'type': 'date'}),
        'end_date': forms.DateInput(attrs={'type': 'date'}),
    },
    extra=1,
    can_delete=True
)

# Household Member FormSet
HouseholdMemberFormSet = forms.inlineformset_factory(
    Application, HouseholdMember,
    fields=['first_name', 'last_name', 'dob', 'relationship', 'is_adult'],
    widgets={'dob': forms.DateInput(attrs={'type': 'date'})},
    extra=1,
    can_delete=True
)

# Reference FormSet
ReferenceFormSet = forms.inlineformset_factory(
    Application, Reference,
    fields=['full_name', 'email', 'phone', 'relationship', 'years_known'],
    extra=2,
    can_delete=False 
)
