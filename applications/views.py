from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Application
from .forms import (
    ApplicationForm, PersonalDetailsForm, AddressEntryFormSet, PremisesForm,
    ChildcareServiceForm, TrainingForm, EmploymentEntryFormSet, HouseholdMemberFormSet,
    SuitabilityForm, DeclarationForm, ReferenceFormSet
)

def register_view(request):
    """
    Handles the multi-step registration form.
    Since the frontend is a single page with JS sections, we handle the final POST submission here.
    """
    if request.method == 'POST':
        # Main application form
        # We might need to handle specific logic if we want to save partial progress, 
        # but for this MVP we'll assume a full submission or create a draft.
        
        # Initialize all forms
        personal_form = PersonalDetailsForm(request.POST, prefix='personal')
        premises_form = PremisesForm(request.POST, prefix='premises')
        service_form = ChildcareServiceForm(request.POST, prefix='service')
        training_form = TrainingForm(request.POST, prefix='training')
        suitability_form = SuitabilityForm(request.POST, prefix='suitability')
        declaration_form = DeclarationForm(request.POST, prefix='declaration')
        
        # FormSets
        address_formset = AddressEntryFormSet(request.POST, prefix='address')
        employment_formset = EmploymentEntryFormSet(request.POST, prefix='employment')
        household_formset = HouseholdMemberFormSet(request.POST, prefix='household')
        reference_formset = ReferenceFormSet(request.POST, prefix='reference')

        # Check validity (simplified for MVP, ideally check all)
        if (personal_form.is_valid() and premises_form.is_valid() and 
            service_form.is_valid() and training_form.is_valid() and 
            suitability_form.is_valid() and declaration_form.is_valid()):
            
            # Create Application instance
            application = Application.objects.create(status='SUBMITTED')
            
            # Save related models
            personal = personal_form.save(commit=False)
            personal.application = application
            personal.save()
            
            premises = premises_form.save(commit=False)
            premises.application = application
            premises.save()
            
            service = service_form.save(commit=False)
            service.application = application
            service.save()
            
            training = training_form.save(commit=False)
            training.application = application
            training.save()
            
            suitability = suitability_form.save(commit=False)
            suitability.application = application
            suitability.save()
            
            declaration = declaration_form.save(commit=False)
            declaration.application = application
            declaration.save()
            
            # Save FormSets
            address_formset.instance = application
            address_formset.save()
            
            employment_formset.instance = application
            employment_formset.save()
            
            household_formset.instance = application
            household_formset.save()
            
            reference_formset.instance = application
            reference_formset.save()
            
            messages.success(request, 'Application submitted successfully!')
            return redirect('dashboard') # Redirect to dashboard or success page
        else:
            messages.error(request, 'Please correct the errors in the form.')
            # In a real scenario, we'd return the forms with errors.
            # For this MVP HTML, we might need to rely on client-side val or render errors.
    
    else:
        # Initialize empty forms
        personal_form = PersonalDetailsForm(prefix='personal')
        premises_form = PremisesForm(prefix='premises')
        service_form = ChildcareServiceForm(prefix='service')
        training_form = TrainingForm(prefix='training')
        suitability_form = SuitabilityForm(prefix='suitability')
        declaration_form = DeclarationForm(prefix='declaration')
        
        address_formset = AddressEntryFormSet(prefix='address')
        employment_formset = EmploymentEntryFormSet(prefix='employment')
        household_formset = HouseholdMemberFormSet(prefix='household')
        reference_formset = ReferenceFormSet(prefix='reference')

    context = {
        'personal_form': personal_form,
        'premises_form': premises_form,
        'service_form': service_form,
        'training_form': training_form,
        'suitability_form': suitability_form,
        'declaration_form': declaration_form,
        'address_formset': address_formset,
        'employment_formset': employment_formset,
        'household_formset': household_formset,
        'reference_formset': reference_formset,
    }
    return render(request, 'applications/register.html', context)
