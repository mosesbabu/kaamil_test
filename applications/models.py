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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Application {self.id} ({self.get_status_display()})"

class PersonalDetails(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='personal_details')
    title = models.CharField(max_length=10)
    first_name = models.CharField(max_length=100)
    middle_names = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    
    dob = models.DateField(verbose_name="Date of Birth")
    gender = models.CharField(max_length=20)
    known_by_other_names = models.BooleanField(default=False)
    
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    ni_number = models.CharField(
        max_length=9, 
        verbose_name="National Insurance Number",
        validators=[RegexValidator(r'^[A-CEGHJ-PR-TW-Z]{1}[A-CEGHJ-NPR-TW-Z]{1}[0-9]{6}[A-D]{1}$', 'Invalid NI number format')]
    )
    right_to_work_status = models.CharField(max_length=100)
    lived_outside_uk = models.BooleanField(default=False)
    military_base_abroad = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class AddressEntry(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='address_history')
    line1 = models.CharField(max_length=255)
    line2 = models.CharField(max_length=255, blank=True, null=True)
    town = models.CharField(max_length=100)
    postcode = models.CharField(max_length=10)
    move_in_date = models.DateField()
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
    local_authority = models.CharField(max_length=100)
    premises_type = models.CharField(max_length=20, choices=PREMISES_TYPES)
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
    
    food_hygiene_completed = models.BooleanField(default=False)
    food_hygiene_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Training for {self.application.id}"

class EmploymentEntry(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='employment_history')
    employer_name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return  f"{self.role} at {self.employer_name}"

class HouseholdMember(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='household_members')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()
    relationship = models.CharField(max_length=100)
    is_adult = models.BooleanField(default=True) # Calculated based on DOB usually, but good to flag

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Reference(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='references')
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    relationship = models.CharField(max_length=100)
    years_known = models.IntegerField()

    def __str__(self):
        return self.full_name

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
    
    signature = models.CharField(max_length=255)
    print_name = models.CharField(max_length=255)
    date_signed = models.DateField()

    def __str__(self):
        return f"Declaration by {self.print_name}"
