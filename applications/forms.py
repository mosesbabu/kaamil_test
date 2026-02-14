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
            'title': forms.Select(attrs={'class': 'select'}),
            'first_name': forms.TextInput(attrs={'class': 'input'}),
            'middle_names': forms.TextInput(attrs={'class': 'input'}),
            'last_name': forms.TextInput(attrs={'class': 'input'}),
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'input input-md'}),
            'gender': forms.RadioSelect(), # Note: Custom rendering in template
            'known_by_other_names': forms.CheckboxInput(attrs={'class': 'checkbox-item'}),
            'email': forms.EmailInput(attrs={'class': 'input', 'placeholder': 'name@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'input', 'placeholder': '07123 456789'}),
            'ni_number': forms.TextInput(attrs={'class': 'input input-md', 'placeholder': 'QQ 12 34 56 C', 'style': 'text-transform: uppercase;'}),
            'right_to_work_status': forms.Select(attrs={'class': 'select'}),
        }

class PremisesForm(forms.ModelForm):
    class Meta:
        model = Premises
        exclude = ['application']
        widgets = {
            'local_authority': forms.TextInput(attrs={'class': 'input', 'id': 'authoritySearch', 'autocomplete': 'off'}),
            'premises_type': forms.RadioSelect(),
            'pets_details': forms.Textarea(attrs={'rows': 3, 'class': 'textarea'}),
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
            'first_aid_date': forms.DateInput(attrs={'type': 'date', 'class': 'input input-md'}),
            'first_aid_org': forms.TextInput(attrs={'class': 'input'}),
            'safeguarding_date': forms.DateInput(attrs={'type': 'date', 'class': 'input input-md'}),
            'safeguarding_org': forms.TextInput(attrs={'class': 'input'}),
            'eyfs_date': forms.DateInput(attrs={'type': 'date', 'class': 'input input-md'}),
            'eyfs_org': forms.TextInput(attrs={'class': 'input'}),
            'food_hygiene_date': forms.DateInput(attrs={'type': 'date', 'class': 'input input-md'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make completion flags optional as they might not be in the UI
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
            'signature': forms.TextInput(attrs={'class': 'input signature-input'}),
            'print_name': forms.TextInput(attrs={'class': 'input'}),
            'date_signed': forms.DateInput(attrs={'type': 'date', 'class': 'input input-md', 'id': 'declarationDate'}),
        }

# Address History FormSet
AddressEntryFormSet = forms.inlineformset_factory(
    Application, AddressEntry,
    fields=['line1', 'line2', 'town', 'postcode', 'move_in_date', 'is_current'],
    widgets={
        'line1': forms.TextInput(attrs={'class': 'input'}),
        'line2': forms.TextInput(attrs={'class': 'input'}),
        'town': forms.TextInput(attrs={'class': 'input'}),
        'postcode': forms.TextInput(attrs={'class': 'input input-sm', 'style': 'text-transform: uppercase;'}),
        'move_in_date': forms.DateInput(attrs={'type': 'date', 'class': 'input input-md'}),
    },
    extra=1,
    can_delete=True
)

# Employment FormSet
EmploymentEntryFormSet = forms.inlineformset_factory(
    Application, EmploymentEntry,
    fields=['employer_name', 'role', 'start_date', 'end_date', 'is_current'],
    widgets={
        'employer_name': forms.TextInput(attrs={'class': 'input'}),
        'role': forms.TextInput(attrs={'class': 'input'}),
        'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'input input-md'}),
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
        'first_name': forms.TextInput(attrs={'class': 'input'}),
        'last_name': forms.TextInput(attrs={'class': 'input'}),
        'dob': forms.DateInput(attrs={'type': 'date', 'class': 'input input-md'}),
        'relationship': forms.TextInput(attrs={'class': 'input'}),
    },
    extra=1,
    can_delete=True
)

# Reference FormSet
ReferenceFormSet = forms.inlineformset_factory(
    Application, Reference,
    fields=['first_name', 'last_name', 'email', 'phone', 'relationship', 'years_known'],
    widgets={
        'first_name': forms.TextInput(attrs={'class': 'input'}),
        'last_name': forms.TextInput(attrs={'class': 'input'}),
        'email': forms.EmailInput(attrs={'class': 'input'}),
        'phone': forms.TextInput(attrs={'class': 'input'}),
        'relationship': forms.TextInput(attrs={'class': 'input'}),
        'years_known': forms.NumberInput(attrs={'class': 'input input-sm'}),
    },
    extra=2,
    can_delete=False 
)
