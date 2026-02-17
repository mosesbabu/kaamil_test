from django.core.management.base import BaseCommand
from applications.models import Application, Premises, ChildcareService, Training, Suitability, Declaration


class Command(BaseCommand):
    help = 'Cleans up empty Premises, ChildcareService, Training, Suitability, and Declaration records that only contain default values'

    def handle(self, *args, **options):
        self.stdout.write('Starting cleanup of empty records...\n')
        
        # Clean up empty Premises
        empty_premises = []
        for premises in Premises.objects.all():
            has_data = (
                premises.local_authority or 
                premises.premises_type or 
                premises.has_outdoor_space or 
                premises.has_pets or 
                premises.pets_details
            )
            if not has_data:
                empty_premises.append(premises.id)
        
        if empty_premises:
            count = Premises.objects.filter(id__in=empty_premises).delete()[0]
            self.stdout.write(self.style.SUCCESS(f'✓ Deleted {count} empty Premises records'))
        else:
            self.stdout.write('  No empty Premises records found')
        
        # Clean up empty ChildcareService
        empty_services = []
        for service in ChildcareService.objects.all():
            has_data = (
                service.care_age_0_5 or 
                service.care_age_5_8 or 
                service.care_age_8_plus or
                service.work_with_assistants or
                service.number_of_assistants > 0
            )
            if not has_data:
                empty_services.append(service.id)
        
        if empty_services:
            count = ChildcareService.objects.filter(id__in=empty_services).delete()[0]
            self.stdout.write(self.style.SUCCESS(f'✓ Deleted {count} empty ChildcareService records'))
        else:
            self.stdout.write('  No empty ChildcareService records found')
        
        # Clean up empty Training
        empty_training = []
        for training in Training.objects.all():
            has_data = (
                training.first_aid_completed or
                training.safeguarding_completed or
                training.eyfs_completed or
                training.level2_qual_completed or
                training.food_hygiene_completed or
                training.first_aid_date or
                training.safeguarding_date
            )
            if not has_data:
                empty_training.append(training.id)
        
        if empty_training:
            count = Training.objects.filter(id__in=empty_training).delete()[0]
            self.stdout.write(self.style.SUCCESS(f'✓ Deleted {count} empty Training records'))
        else:
            self.stdout.write('  No empty Training records found')
        
        # Clean up empty Suitability
        empty_suitability = []
        for suitability in Suitability.objects.all():
            has_data = (
                suitability.has_medical_condition or
                suitability.is_disqualified or
                suitability.social_services_involved or
                suitability.has_dbs or
                suitability.medical_condition_details or
                suitability.social_services_details or
                suitability.dbs_number
            )
            if not has_data:
                empty_suitability.append(suitability.id)
        
        if empty_suitability:
            count = Suitability.objects.filter(id__in=empty_suitability).delete()[0]
            self.stdout.write(self.style.SUCCESS(f'✓ Deleted {count} empty Suitability records'))
        else:
            self.stdout.write('  No empty Suitability records found')
        
        # Clean up empty Declaration
        empty_declaration = []
        for declaration in Declaration.objects.all():
            has_data = (
                declaration.consent_auth_contact or
                declaration.consent_auth_share or
                declaration.consent_understand_usage or
                declaration.consent_understand_gdpr or
                declaration.consent_truth or
                declaration.signature or
                declaration.print_name or
                declaration.date_signed
            )
            if not has_data:
                empty_declaration.append(declaration.id)
        
        if empty_declaration:
            count = Declaration.objects.filter(id__in=empty_declaration).delete()[0]
            self.stdout.write(self.style.SUCCESS(f'✓ Deleted {count} empty Declaration records'))
        else:
            self.stdout.write('  No empty Declaration records found')
        
        self.stdout.write(self.style.SUCCESS('\n✓ Cleanup complete!'))
