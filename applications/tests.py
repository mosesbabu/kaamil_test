from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from applications.models import (
    Application, PersonalDetails, Premises, ChildcareService,
    Training, Suitability, Declaration, AddressEntry
)
from applications.forms import (
    PersonalDetailsForm, TrainingForm, AddressEntryFormSet
)

class ModelTests(TestCase):
    def test_application_creation(self):
        """Test that an application is created with default status DRAFT."""
        app = Application.objects.create()
        self.assertEqual(app.status, 'DRAFT')
        self.assertTrue(isinstance(app, Application))
        self.assertEqual(str(app), f"Application {app.id} (Draft)")

class FormTests(TestCase):
    def test_personal_details_form_valid(self):
        """Test PersonalDetailsForm with valid data."""
        form_data = {
            'title': 'Mr',
            'first_name': 'John',
            'last_name': 'Doe',
            'dob': '1990-01-01',
            'gender': 'Male',
            'email': 'john@example.com',
            'phone': '07123456789',
            'ni_number': 'AB123456C',
            'right_to_work_status': 'British Citizen',
            'lived_outside_uk': False,
            'military_base_abroad': False,
        }
        form = PersonalDetailsForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_personal_details_form_qq_ni(self):
        """Test PersonalDetailsForm with 'QQ' NI number which was previously failing."""
        form_data = {
            'title': 'Mr',
            'first_name': 'John',
            'last_name': 'Doe',
            'dob': '1990-01-01',
            'gender': 'Male',
            'email': 'john@example.com',
            'phone': '07123456789',
            'ni_number': 'QQ123456C',
            'right_to_work_status': 'British Citizen',
            'lived_outside_uk': False,
            'military_base_abroad': False,
        }
        form = PersonalDetailsForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_training_form_optional_flags(self):
        """Test that completion flags in TrainingForm are optional."""
        # Only providing date/org data, no boolean flags (which should default or be ignored if optional)
        # Actually the model defaults are False, form fields are checkboxes.
        # If required=False, they can be missing from POST data.
        form_data = {
            'first_aid_date': '2023-01-01',
            'first_aid_org': 'Red Cross',
        }
        form = TrainingForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)
        # Verify cleaning doesn't fail on missing booleans
        self.assertFalse(form.cleaned_data.get('first_aid_completed'))

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.dashboard_url = reverse('dashboard')

    def test_dashboard_view_get(self):
        """Test the dashboard view returns 200 and expected context."""
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('applications', response.context)
        self.assertIn('total_apps', response.context)

    def test_register_view_get(self):
        """Test the register view returns 200 and contains forms."""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('personal_form', response.context)
        self.assertIn('premises_form', response.context)

    def test_register_view_post_success(self):
        """Test a successful application submission."""
        # We need comprehensive data for all forms and formsets
        data = {
            # ApplicationForm (status is not in form fields, handled in view)
            
            # PersonalDetailsForm (prefix='personal')
            'personal-title': 'Mrs',
            'personal-first_name': 'Jane',
            'personal-last_name': 'Smith',
            'personal-dob': '1985-05-20',
            'personal-gender': 'Female',
            'personal-email': 'jane@example.com',
            'personal-phone': '07987654321',
            'personal-ni_number': 'AB123456C',
            'personal-right_to_work_status': 'British Citizen',
            
            # PremisesForm (prefix='premises')
            'premises-local_authority': 'Leeds',
            'premises-premises_type': 'Domestic',
            'premises-is_own_home': 'on',
            
            # ChildcareServiceForm (prefix='service')
            # (boolean fields can be omitted if false, assuming checkboxes)
            'service-number_of_assistants': '0',
            
            # TrainingForm (prefix='training')
            # Empty is valid as they are verified later or optional in initial form
            
            # SuitabilityForm (prefix='suitability')
            # Empty valid for booleans default False
            
            # DeclarationForm (prefix='declaration')
            'declaration-signature': 'Jane Smith',
            'declaration-print_name': 'Jane Do Smith',
            'declaration-date_signed': timezone.now().date(),
            
            # FormSets - Management Forms are critical
            'address-TOTAL_FORMS': '1',
            'address-INITIAL_FORMS': '0',
            'address-MIN_NUM_FORMS': '0',
            'address-MAX_NUM_FORMS': '1000',
            
            'address-0-line1': '123 Fake St',
            'address-0-town': 'Leeds',
            'address-0-postcode': 'LS1 1AA',
            'address-0-move_in_date': '2020-01-01',
            
            'employment-TOTAL_FORMS': '1',
            'employment-INITIAL_FORMS': '0',
            'employment-MIN_NUM_FORMS': '0',
            'employment-MAX_NUM_FORMS': '1000',
            
            'employment-0-employer_name': 'Self',
            'employment-0-role': 'Nanny',
            'employment-0-start_date': '2015-01-01',
            
            'household-TOTAL_FORMS': '1',
            'household-INITIAL_FORMS': '0',
            'household-MIN_NUM_FORMS': '0',
            'household-MAX_NUM_FORMS': '1000',
            'household-0-first_name': 'Partner',
            'household-0-last_name': 'Smith',
            'household-0-dob': '1980-01-01',
            'household-0-relationship': 'Husband',
            
            'reference-TOTAL_FORMS': '2',
            'reference-INITIAL_FORMS': '0',
            'reference-MIN_NUM_FORMS': '0',
            'reference-MAX_NUM_FORMS': '1000',
            
            'reference-0-first_name': 'Ref1',
            'reference-0-last_name': 'Person',
            'reference-0-email': 'ref1@example.com',
            'reference-0-phone': '0111111111',
            'reference-0-relationship': 'Friend',
            'reference-0-years_known': '5',
            
            'reference-1-first_name': 'Ref2',
            'reference-1-last_name': 'Person',
            'reference-1-email': 'ref2@example.com',
            'reference-1-phone': '0222222222',
            'reference-1-relationship': 'Colleague',
            'reference-1-years_known': '3',
        }
        
        response = self.client.post(self.register_url, data)
        
        # Check for redirect (success)
        if response.status_code != 302:
            # If fail, print form errors from context if available
            # print(response.context.get('personal_form').errors)
            pass
            
        self.assertRedirects(response, self.dashboard_url)
        self.assertEqual(Application.objects.count(), 1)
        self.assertEqual(Application.objects.first().status, 'SUBMITTED')
