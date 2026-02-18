from django.contrib import admin
from .models import (
    Application, PersonalDetails, AddressEntry, Premises,
    ChildcareService, Training, EmploymentEntry, HouseholdMember,
    Suitability, Declaration, Reference
)

class PersonalDetailsInline(admin.StackedInline):
    model = PersonalDetails
    extra = 0

class AddressEntryInline(admin.TabularInline):
    model = AddressEntry
    extra = 0

class PremisesInline(admin.StackedInline):
    model = Premises
    extra = 0

class ChildcareServiceInline(admin.StackedInline):
    model = ChildcareService
    extra = 0

class TrainingInline(admin.StackedInline):
    model = Training
    extra = 0

class SuitabilityInline(admin.StackedInline):
    model = Suitability
    extra = 0

class DeclarationInline(admin.StackedInline):
    model = Declaration
    extra = 0

class EmploymentEntryInline(admin.TabularInline):
    model = EmploymentEntry
    extra = 0

class HouseholdMemberInline(admin.TabularInline):
    model = HouseholdMember
    extra = 0

class ReferenceInline(admin.TabularInline):
    model = Reference
    extra = 0

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['application_number', 'get_applicant_name', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['application_number', 'personal_details__first_name', 'personal_details__last_name', 'personal_details__email']
    readonly_fields = ['id', 'application_number', 'created_at', 'updated_at']
    
    inlines = [
        PersonalDetailsInline,
        AddressEntryInline,
        PremisesInline,
        ChildcareServiceInline,
        TrainingInline,
        EmploymentEntryInline,
        HouseholdMemberInline,
        ReferenceInline,
        SuitabilityInline,
        DeclarationInline,
    ]
    
    def get_applicant_name(self, obj):
        if hasattr(obj, 'personal_details'):
            return f"{obj.personal_details.first_name} {obj.personal_details.last_name}"
        return "N/A"
    get_applicant_name.short_description = 'Applicant Name'
