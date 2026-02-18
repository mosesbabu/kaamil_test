from django.db import migrations
from django.utils import timezone

def backfill_application_numbers(apps, schema_editor):
    Application = apps.get_model('applications', 'Application')
    # Use order_by to ensure sequential numbering based on creation date
    for app in Application.objects.filter(application_number__isnull=True).order_by('created_at'):
        year = app.created_at.year if app.created_at else timezone.now().year
        prefix = f'RK-{year}-'
        
        # Find the max sequence for this year so far in this migration
        last = (
            Application.objects
            .filter(application_number__startswith=prefix)
            .order_by('application_number')
            .values_list('application_number', flat=True)
            .last()
        )
        
        if last:
            try:
                seq = int(last.split('-')[-1]) + 1
            except (ValueError, IndexError):
                seq = 1
        else:
            seq = 1
            
        app.application_number = f'{prefix}{seq:05d}'
        app.save()

class Migration(migrations.Migration):
    dependencies = [
        ('applications', '0008_add_application_number'), # This depends on the field creation migration
    ]

    operations = [
        migrations.RunPython(backfill_application_numbers),
    ]
