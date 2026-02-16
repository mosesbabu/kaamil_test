import json
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
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
    # Try to get application from GET param or session
    app_id = request.GET.get('app_id') or request.session.get('application_id')
    application = None
    if app_id:
        application = Application.objects.filter(id=app_id).first()
        if application:
            request.session['application_id'] = str(application.id)

    if request.method == 'POST':
        action = request.POST.get('action', 'submit')
        is_draft = (action == 'save_and_exit')
        
        # Initialize all forms
        personal_form = PersonalDetailsForm(request.POST, prefix='personal', instance=application.personal_details if application and hasattr(application, 'personal_details') else None, is_draft=is_draft)
        premises_form = PremisesForm(request.POST, prefix='premises', instance=application.premises if application and hasattr(application, 'premises') else None, is_draft=is_draft)
        service_form = ChildcareServiceForm(request.POST, prefix='service', instance=application.service_details if application and hasattr(application, 'service_details') else None, is_draft=is_draft)
        training_form = TrainingForm(request.POST, prefix='training', instance=application.training if application and hasattr(application, 'training') else None, is_draft=is_draft)
        suitability_form = SuitabilityForm(request.POST, prefix='suitability', instance=application.suitability if application and hasattr(application, 'suitability') else None, is_draft=is_draft)
        declaration_form = DeclarationForm(request.POST, prefix='declaration', instance=application.declaration if application and hasattr(application, 'declaration') else None, is_draft=is_draft)
        
        # FormSets with dynamic extra forms
        def get_formset(factory, prefix, application):
            already_exists = False
            if application:
                # Check if any related objects exist for this application
                # This is a bit generic but works if we know the related name or just check the count
                # Inline formsets have a 'queryset' attribute we can check
                qs = factory.model.objects.filter(application=application)
                if qs.exists():
                    already_exists = True
            
            # Create a temporary factory with 0 extra if objects already exist
            # but preserve weights and fields from the original factory
            if already_exists:
                # We can override the extra attribute on the class or just re-create it
                # A simpler trick: set the extra attribute on the instance after creation
                fs = factory(request.POST, prefix=prefix, instance=application)
                fs.extra = 0
                return fs
            return factory(request.POST, prefix=prefix, instance=application)

        address_formset = get_formset(AddressEntryFormSet, 'address', application)
        employment_formset = get_formset(EmploymentEntryFormSet, 'employment', application)
        household_formset = get_formset(HouseholdMemberFormSet, 'household', application)
        reference_formset = get_formset(ReferenceFormSet, 'reference', application)

        if action == 'save_and_exit':
            # Partial save - don't enforce full validation
            if not application:
                application = Application.objects.create(status='DRAFT')
                request.session['application_id'] = str(application.id)
                # Update formset instances
                address_formset.instance = application
                employment_formset.instance = application
                household_formset.instance = application
                reference_formset.instance = application
            
            # Save whatever we have
            def save_partial(form, app):
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.application = app
                    obj.save()
                else:
                    # Even if invalid, we might want to save what's there?
                    # Django ModelForms don't easily save invalid data.
                    # But since we made fields null=True in models, 
                    # we should update forms.py to make them not required if it's a draft.
                    # For now, we'll try to save if it passes whatever relaxed validation we have.
                    pass

            # Save main forms
            for f in [personal_form, premises_form, service_form, training_form, suitability_form, declaration_form]:
                save_partial(f, application)
            
            # Save formsets
            for fs in [address_formset, employment_formset, household_formset, reference_formset]:
                if fs.is_valid():
                    fs.save()
            
            # Update application-level flags
            try:
                current_section = int(request.POST.get('current_section', 0))
                application.last_section_completed = max(application.last_section_completed, current_section)
                
                # New Household flags
                if 'application-has_adults_in_home' in request.POST:
                    application.has_adults_in_home = request.POST.get('application-has_adults_in_home') == 'True'
                if 'application-has_children_in_home' in request.POST:
                    application.has_children_in_home = request.POST.get('application-has_children_in_home') == 'True'
                
                application.save()
            except Exception as e:
                print(f"Error saving application flags: {e}")
                pass

            messages.success(request, 'Progress saved successfully. You can complete your application later.')
            return redirect('dashboard')

        # Full submit logic
        # Check validity of ALL forms and formsets
        forms_valid = (personal_form.is_valid() and premises_form.is_valid() and 
            service_form.is_valid() and training_form.is_valid() and 
            suitability_form.is_valid() and declaration_form.is_valid())
        
        formsets_valid = (address_formset.is_valid() and employment_formset.is_valid() and
            household_formset.is_valid() and reference_formset.is_valid())
        
        if forms_valid and formsets_valid:
            if not application:
                application = Application.objects.create(status='SUBMITTED')
                # Update formset instances if the application was just created
                address_formset.instance = application
                employment_formset.instance = application
                household_formset.instance = application
                reference_formset.instance = application
            else:
                application.status = 'SUBMITTED'
                
                # New Household flags
                if 'application-has_adults_in_home' in request.POST:
                    application.has_adults_in_home = request.POST.get('application-has_adults_in_home') == 'True'
                if 'application-has_children_in_home' in request.POST:
                    application.has_children_in_home = request.POST.get('application-has_children_in_home') == 'True'
                
                application.save()
            
            # Save everything
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
            
            address_formset.save()
            employment_formset.save()
            household_formset.save()
            reference_formset.save()
            
            # Clear session
            if 'application_id' in request.session:
                del request.session['application_id']
            
            messages.success(request, 'Application submitted successfully!')
            return redirect('dashboard') # Redirect to dashboard or success page
        else:
            # Collect and log all errors for debugging
            all_errors = []
            for form_name, form_obj in [
                ('personal', personal_form), ('premises', premises_form),
                ('service', service_form), ('training', training_form),
                ('suitability', suitability_form), ('declaration', declaration_form),
            ]:
                if not form_obj.is_valid():
                    all_errors.append(f"{form_name}: {form_obj.errors}")
            for fs_name, fs_obj in [
                ('address', address_formset), ('employment', employment_formset),
                ('household', household_formset), ('reference', reference_formset),
            ]:
                if not fs_obj.is_valid():
                    all_errors.append(f"{fs_name}: {fs_obj.errors}")
            
            print("=" * 60)
            print("FORM VALIDATION ERRORS:")
            for err in all_errors:
                print(f"  {err}")
            print("=" * 60)
            
            messages.error(request, 'Please correct the errors in the form.')
    
    else:
        # Initialize forms from session if exist
        personal_form = PersonalDetailsForm(prefix='personal', instance=application.personal_details if application and hasattr(application, 'personal_details') else None)
        premises_form = PremisesForm(prefix='premises', instance=application.premises if application and hasattr(application, 'premises') else None)
        service_form = ChildcareServiceForm(prefix='service', instance=application.service_details if application and hasattr(application, 'service_details') else None)
        training_form = TrainingForm(prefix='training', instance=application.training if application and hasattr(application, 'training') else None)
        suitability_form = SuitabilityForm(prefix='suitability', instance=application.suitability if application and hasattr(application, 'suitability') else None)
        declaration_form = DeclarationForm(prefix='declaration', instance=application.declaration if application and hasattr(application, 'declaration') else None)
        
        # FormSets for GET requests (Resume)
        def get_formset_get(factory, prefix, application):
            extra = factory.extra # default from factory
            if application:
                qs = factory.model.objects.filter(application=application)
                if qs.exists():
                    extra = 0
            
            # Create a localized version of the factory or just override extra on the instance
            fs = factory(prefix=prefix, instance=application)
            fs.extra = extra
            return fs

        address_formset = get_formset_get(AddressEntryFormSet, 'address', application)
        employment_formset = get_formset_get(EmploymentEntryFormSet, 'employment', application)
        household_formset = get_formset_get(HouseholdMemberFormSet, 'household', application)
        reference_formset = get_formset_get(ReferenceFormSet, 'reference', application)

    context = {
        'application': application,
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

def dashboard_view(request):
    """
    Rich dashboard matching cma-portal-v2.html design.
    Passes application data as JSON for JavaScript-driven detail panel.
    """
    applications = Application.objects.select_related(
        'personal_details', 'premises', 'training', 'suitability', 'declaration'
    ).prefetch_related(
        'references', 'household_members', 'employment_history', 'address_history'
    ).all().order_by('-created_at')
    
    # Stats
    total_apps = applications.count()
    submitted_apps = applications.filter(status='SUBMITTED').count()
    draft_apps = applications.filter(status='DRAFT').count()
    registered_apps = applications.filter(status='REGISTERED').count()
    
    # Logic for stats cards
    require_action_apps = submitted_apps  # For now, all submitted apps require action
    in_progress_apps = applications.filter(status__in=['CHECKS_IN_PROGRESS', 'UNDER_REVIEW']).count()
    completed_apps = registered_apps # YTD logic could be added here
    
    # Count all connected persons across all applications
    from .models import HouseholdMember
    total_connected_persons = HouseholdMember.objects.filter(application__in=applications).count()
    
    # Serialize applications to JSON for the JS detail panel
    apps_json = []
    from django.utils import timezone
    now = timezone.now()

    for app in applications:
        days_in_stage = (now.date() - app.updated_at.date()).days if app.updated_at else 0
        
        app_data = {
            'id': str(app.id), # Ensure string for JS
            'status': app.status,
            'status_display': app.get_status_display(),
            'created_at': app.created_at.strftime('%Y-%m-%d %H:%M') if app.created_at else '',
            'updated_at': app.updated_at.strftime('%Y-%m-%d %H:%M') if app.updated_at else '',
            'daysInStage': days_in_stage,
            'risk': 'high' if days_in_stage > 14 else 'low', # Mock risk logic
        }
        
        # Personal Details
        try:
            pd = app.personal_details
            app_data['personal'] = {
                'title': pd.title,
                'first_name': pd.first_name,
                'middle_names': pd.middle_names or '',
                'last_name': pd.last_name,
                'dob': pd.dob.strftime('%Y-%m-%d') if pd.dob else '',
                'gender': pd.gender,
                'email': pd.email,
                'phone': pd.phone,
                'ni_number': pd.ni_number,
                'right_to_work_status': pd.right_to_work_status,
                'known_by_other_names': pd.known_by_other_names,
                'lived_outside_uk': pd.lived_outside_uk,
                'military_base_abroad': pd.military_base_abroad,
            }
        except Exception:
            app_data['personal'] = None
        
        # Premises
        try:
            pr = app.premises
            app_data['premises'] = {
                'local_authority': pr.local_authority,
                'premises_type': pr.premises_type,
                'is_own_home': pr.is_own_home,
                'has_outdoor_space': pr.has_outdoor_space,
                'has_pets': pr.has_pets,
                'pets_details': pr.pets_details or '',
            }
            app_data['local_authority'] = pr.local_authority # Flatten for table
        except Exception:
            app_data['premises'] = None
            app_data['local_authority'] = '-'
        
        # Training
        try:
            tr = app.training
            app_data['training'] = {
                'first_aid_completed': tr.first_aid_completed,
                'first_aid_date': tr.first_aid_date.strftime('%Y-%m-%d') if tr.first_aid_date else '',
                'first_aid_org': tr.first_aid_org or '',
                'safeguarding_completed': tr.safeguarding_completed,
                'safeguarding_date': tr.safeguarding_date.strftime('%Y-%m-%d') if tr.safeguarding_date else '',
                'safeguarding_org': tr.safeguarding_org or '',
                'eyfs_completed': tr.eyfs_completed,
                'food_hygiene_completed': tr.food_hygiene_completed,
            }
        except Exception:
            app_data['training'] = None
        
        # Suitability & Checks Construction
        checks = {
            'dbs': {'status': 'not-started', 'details': ''},
            'la_check': {'status': 'not-started'},
            'ofsted': {'status': 'not-started'},
            'gp_health': {'status': 'not-started'},
            'ref_1': {'status': 'not-started'},
            'ref_2': {'status': 'not-started'},
            'first_aid': {'status': 'not-started'},
            'safeguarding': {'status': 'not-started'},
        }

        try:
            su = app.suitability
            app_data['suitability'] = {
                'has_medical_condition': su.has_medical_condition,
                'is_disqualified': su.is_disqualified,
                'social_services_involved': su.social_services_involved,
                'has_dbs': su.has_dbs,
                'dbs_number': su.dbs_number or '',
            }
            if su.has_dbs:
                checks['dbs'] = {'status': 'complete', 'details': su.dbs_number}
            elif su.dbs_number:
                 checks['dbs'] = {'status': 'pending'}
        except Exception:
            app_data['suitability'] = None
        
        # Update checks based on training
        if app_data['training']:
            if app_data['training']['first_aid_completed']: checks['first_aid']['status'] = 'complete'
            if app_data['training']['safeguarding_completed']: checks['safeguarding']['status'] = 'complete'

        # References
        refs = []
        ref_count = 0
        for ref in app.references.all():
            ref_count += 1
            refs.append({
                'full_name': f"{ref.first_name} {ref.last_name}",
                'email': ref.email,
                'phone': ref.phone,
                'relationship': ref.relationship,
                'years_known': ref.years_known,
            })
            if ref_count == 1: checks['ref_1']['status'] = 'pending' # Mock logic
            if ref_count == 2: checks['ref_2']['status'] = 'pending'
            
        app_data['references'] = refs
        app_data['checks'] = checks # Add checks to app_data
        
        # Household Members
        members = []
        for m in app.household_members.all():
            members.append({
                'id': str(m.id),
                'first_name': m.first_name,
                'last_name': m.last_name,
                'dob': m.dob.strftime('%Y-%m-%d') if m.dob else '',
                'relationship': m.relationship,
                'is_adult': m.is_adult,
                'checks': {} # Mock checks for persons
            })
        app_data['household_members'] = members
        # Service Details (Registers)
        try:
            sd = app.service_details
            registers = []
            if sd.care_age_0_5: registers.append('Early Years')
            if sd.care_age_5_8: registers.append('Compulsory Childcare')
            if sd.care_age_8_plus: registers.append('Voluntary Childcare')
            app_data['register'] = registers
        except Exception:
            app_data['register'] = []
        
        # Addresses
        addresses = []
        for addr in app.address_history.all():
            addresses.append({
                'line1': addr.line1,
                'line2': addr.line2 or '',
                'town': addr.town,
                'postcode': addr.postcode,
                'move_in_date': addr.move_in_date.strftime('%Y-%m-%d') if addr.move_in_date else '',
                'is_current': addr.is_current,
            })
        app_data['addresses'] = addresses
        
        apps_json.append(app_data)
    
    context = {
        'applications': applications,
        'total_apps': total_apps,
        'submitted_apps': submitted_apps,
        'draft_apps': draft_apps,
        'registered_apps': registered_apps,
        'require_action_apps': require_action_apps,
        'in_progress_apps': in_progress_apps,
        'completed_apps': completed_apps,
        'total_connected_persons': total_connected_persons,
        'apps_json': json.dumps(apps_json, default=str),
    }
    return render(request, 'applications/dashboard.html', context)
