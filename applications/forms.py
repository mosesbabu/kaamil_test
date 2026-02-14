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
            'title': forms.Select(attrs={'class': 'select', 'required': 'true'}),
            'first_name': forms.TextInput(attrs={'class': 'input', 'required': 'true'}),
            'middle_names': forms.TextInput(attrs={'class': 'input'}), # Optional field
            'last_name': forms.TextInput(attrs={'class': 'input', 'required': 'true'}),
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'input input-md', 'required': 'true'}),
            'gender': forms.RadioSelect(), # Custom rendering
            'known_by_other_names': forms.CheckboxInput(attrs={'class': 'checkbox-item', 'required': 'true'}),
            'email': forms.EmailInput(attrs={'class': 'input', 'placeholder': 'name@example.com', 'required': 'true'}),
            'phone': forms.TextInput(attrs={'class': 'input', 'placeholder': '07123 456789', 'required': 'true'}),
            'ni_number': forms.TextInput(attrs={'class': 'input input-md', 'placeholder': 'QQ 12 34 56 C', 'style': 'text-transform: uppercase;'}),
            'right_to_work_status': forms.Select(attrs={'class': 'select', 'required': 'true'}),
        }

class PremisesForm(forms.ModelForm):
    class Meta:
        model = Premises
        exclude = ['application']
        widgets = {
            'local_authority': forms.TextInput(attrs={'class': 'input', 'id': 'authoritySearch', 'autocomplete': 'off', 'required': 'true'}),
            'premises_type': forms.RadioSelect(),
            'pets_details': forms.Textarea(attrs={'rows': 3, 'class': 'textarea'}), # Optional
        }

class ChildcareServiceForm(forms.ModelForm):
    class Meta:
        model = ChildcareService
        exclude = ['application']
        widgets = {
            'number_of_assistants': forms.NumberInput(attrs={'class': 'input input-sm'}),
        }

class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        exclude = ['application']
        widgets = {
            'first_aid_date': forms.DateInput(attrs={'type': 'date', 'class': 'input input-md', 'required': 'true'}),
            'first_aid_org': forms.TextInput(attrs={'class': 'input', 'required': 'true'}),
            'safeguarding_date': forms.DateInput(attrs={'type': 'date', 'class': 'input input-md', 'required': 'true'}),
            'safeguarding_org': forms.TextInput(attrs={'class': 'input', 'required': 'true'}),
            'eyfs_date': forms.DateInput(attrs={'type': 'date', 'class': 'input input-md'}),
            'eyfs_org': forms.TextInput(attrs={'class': 'input'}),
            'food_hygiene_date': forms.DateInput(attrs={'type': 'date', 'class': 'input input-md'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in ['first_aid_completed', 'safeguarding_completed', 'eyfs_completed', 'food_hygiene_completed']:
            if field in self.fields:
                self.fields[field].required = False

class SuitabilityForm(forms.ModelForm):
    class Meta:
        model = Suitability
        exclude = ['application']
        widgets = {
            'medical_condition_details': forms.Textarea(attrs={'rows': 4, 'class': 'textarea'}),
            'social_services_details': forms.Textarea(attrs={'rows': 4, 'class': 'textarea'}),
            'dbs_number': forms.TextInput(attrs={'class': 'input input-md'}),
        }

class DeclarationForm(forms.ModelForm):
    class Meta:
        model = Declaration
        exclude = ['application']
        widgets = {
            'signature': forms.TextInput(attrs={'class': 'input signature-input', 'required': 'true'}),
            'print_name': forms.TextInput(attrs={'class': 'input', 'required': 'true'}),
            'date_signed': forms.DateInput(attrs={'type': 'date', 'class': 'input input-md', 'id': 'declarationDate', 'required': 'true'}),
        }

# Address History FormSet
AddressEntryFormSet = forms.inlineformset_factory(
    Application, AddressEntry,
    fields=['line1', 'line2', 'town', 'postcode', 'move_in_date', 'is_current'],
    widgets={
        'line1': forms.TextInput(attrs={'class': 'input', 'required': 'true'}),
        'line2': forms.TextInput(attrs={'class': 'input'}),
        'town': forms.TextInput(attrs={'class': 'input', 'required': 'true'}),
        'postcode': forms.TextInput(attrs={'class': 'input input-sm', 'style': 'text-transform: uppercase;', 'required': 'true'}),
        'move_in_date': forms.DateInput(attrs={'type': 'date', 'class': 'input input-md', 'required': 'true'}),
    },
    extra=1,
    can_delete=True
)

# Employment FormSet
EmploymentEntryFormSet = forms.inlineformset_factory(
    Application, EmploymentEntry,
    fields=['employer_name', 'role', 'start_date', 'end_date', 'is_current'],
    widgets={
        'employer_name': forms.TextInput(attrs={'class': 'input', 'required': 'true'}),
        'role': forms.TextInput(attrs={'class': 'input', 'required': 'true'}),
        'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'input input-md', 'required': 'true'}),
        'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'input input-md'}),
    },
    extra=1,
    can_delete=True
)

# Household Member FormSet
HouseholdMemberFormSet = forms.inlineformset_factory(
    Application, HouseholdMember,
    fields=['first_name', 'last_name', 'dob', 'relationship', 'is_adult'],
    widgets={
        'first_name': forms.TextInput(attrs={'class': 'input', 'required': 'true'}),
        'last_name': forms.TextInput(attrs={'class': 'input', 'required': 'true'}),
        'dob': forms.DateInput(attrs={'type': 'date', 'class': 'input input-md', 'required': 'true'}),
        'relationship': forms.TextInput(attrs={'class': 'input', 'required': 'true'}),
    },
    extra=1,
    can_delete=True
)

# Reference FormSet
ReferenceFormSet = forms.inlineformset_factory(
    Application, Reference,
    fields=['first_name', 'last_name', 'email', 'phone', 'relationship', 'years_known'],
    widgets={
        'first_name': forms.TextInput(attrs={'class': 'input', 'required': 'true'}),
        'last_name': forms.TextInput(attrs={'class': 'input', 'required': 'true'}),
        'email': forms.EmailInput(attrs={'class': 'input', 'required': 'true'}),
        'phone': forms.TextInput(attrs={'class': 'input', 'required': 'true'}),
        'relationship': forms.TextInput(attrs={'class': 'input', 'required': 'true'}),
        'years_known': forms.NumberInput(attrs={'class': 'input input-sm', 'required': 'true'}),
    },
    extra=2,
    can_delete=False 
)
