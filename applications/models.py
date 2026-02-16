from django.db import models
from django.core.validators import RegexValidator
import uuid

class Application(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('SUBMITTED', 'Submitted'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    last_section_completed = models.IntegerField(default=0)
    has_adults_in_home = models.BooleanField(default=False)
    has_children_in_home = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Application {self.id} ({self.get_status_display()})"

class PersonalDetails(models.Model):
    TITLE_CHOICES = [
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
        ('Miss', 'Miss'),
        ('Ms', 'Ms'),
        ('Mx', 'Mx'),
        ('Dr', 'Dr'),
        ('Other', 'Other'),
    ]
    
    RIGHT_TO_WORK_CHOICES = [
        ('British Citizen', 'British Citizen'),
        ('Irish Citizen', 'Irish Citizen'),
        ('EU Settled Status', 'EU Settled Status'),
        ('EU Pre-settled Status', 'EU Pre-settled Status'),
        ('Visa / Work Permit', 'Visa / Work Permit'),
    ]

    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='personal_details')
    title = models.CharField(max_length=10, choices=TITLE_CHOICES, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    middle_names = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    
    dob = models.DateField(verbose_name="Date of Birth", null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    known_by_other_names = models.BooleanField(default=False)
    
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    ni_number = models.CharField(
        max_length=9, 
        verbose_name="National Insurance Number",
        validators=[RegexValidator(r'^[A-Z]{2}[0-9]{6}[A-D]{1}$', 'Invalid NI number format')],
        null=True, blank=True
    )
    right_to_work_status = models.CharField(max_length=100, choices=RIGHT_TO_WORK_CHOICES, null=True, blank=True)
    lived_outside_uk = models.BooleanField(default=False)
    military_base_abroad = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class AddressEntry(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='address_history')
    line1 = models.CharField(max_length=255, null=True, blank=True)
    line2 = models.CharField(max_length=255, blank=True, null=True)
    town = models.CharField(max_length=100, null=True, blank=True)
    postcode = models.CharField(max_length=10, null=True, blank=True)
    move_in_date = models.DateField(null=True, blank=True)
    move_out_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-move_in_date']

    def __str__(self):
        return f"{self.line1}, {self.postcode}"

class Premises(models.Model):
    PREMISES_TYPES = [
        ('Domestic', 'Domestic (Home)'),
        ('Non-domestic', 'Non-domestic'),
    ]

    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='premises')
    local_authority = models.CharField(max_length=100, null=True, blank=True)
    premises_type = models.CharField(max_length=20, choices=PREMISES_TYPES, null=True, blank=True)
    is_own_home = models.BooleanField(default=True)
    
    # New fields for Section 3
    has_outdoor_space = models.BooleanField(default=False)
    has_pets = models.BooleanField(default=False)
    pets_details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.premises_type} - {self.local_authority}"

class ChildcareService(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='service_details')
    # Age groups (stored as comma-separated or boolean fields - boolean is cleaner)
    care_age_0_5 = models.BooleanField(default=False, verbose_name="0-5 years")
    care_age_5_8 = models.BooleanField(default=False, verbose_name="5-7 years")
    care_age_8_plus = models.BooleanField(default=False, verbose_name="8+ years")
    
    work_with_assistants = models.BooleanField(default=False)
    number_of_assistants = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Service Details for {self.application.id}"

class Training(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='training')
    
    first_aid_completed = models.BooleanField(default=False)
    first_aid_date = models.DateField(blank=True, null=True)
    first_aid_org = models.CharField(max_length=255, blank=True, null=True)
    
    safeguarding_completed = models.BooleanField(default=False)
    safeguarding_date = models.DateField(blank=True, null=True)
    safeguarding_org = models.CharField(max_length=255, blank=True, null=True)
    
    eyfs_completed = models.BooleanField(default=False)
    eyfs_date = models.DateField(blank=True, null=True)
    eyfs_org = models.CharField(max_length=255, blank=True, null=True)
    eyfs_course_title = models.CharField(max_length=255, blank=True, null=True)
    
    level2_qual_completed = models.BooleanField(default=False)
    level2_qual_date = models.DateField(blank=True, null=True)
    level2_qual_org = models.CharField(max_length=255, blank=True, null=True)
    
    food_hygiene_completed = models.BooleanField(default=False)
    food_hygiene_date = models.DateField(blank=True, null=True)
    food_hygiene_org = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Training for {self.application.id}"

class EmploymentEntry(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='employment_history')
    employer_name = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return  f"{self.role} at {self.employer_name}"

class HouseholdMember(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='household_members')
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    relationship = models.CharField(max_length=100, null=True, blank=True)
    is_adult = models.BooleanField(default=True) # Calculated based on DOB usually, but good to flag

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Reference(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='references')
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    relationship = models.CharField(max_length=100, null=True, blank=True)
    years_known = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Suitability(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='suitability')
    
    has_medical_condition = models.BooleanField(default=False)
    medical_condition_details = models.TextField(blank=True, null=True)
    
    is_disqualified = models.BooleanField(default=False)
    social_services_involved = models.BooleanField(default=False)
    social_services_details = models.TextField(blank=True, null=True)
    
    has_dbs = models.BooleanField(default=False)
    dbs_number = models.CharField(max_length=12, blank=True, null=True)

    def __str__(self):
        return f"Suitability for {self.application.id}"

class Declaration(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='declaration')
    consent_auth_contact = models.BooleanField(default=False)
    consent_auth_share = models.BooleanField(default=False)
    consent_understand_usage = models.BooleanField(default=False)
    consent_understand_gdpr = models.BooleanField(default=False)
    consent_truth = models.BooleanField(default=False)
    
    signature = models.CharField(max_length=255, null=True, blank=True)
    print_name = models.CharField(max_length=255, null=True, blank=True)
    date_signed = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Declaration by {self.print_name}"
