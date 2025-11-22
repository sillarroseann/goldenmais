from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_add_tracking_fields'),
    ]

    # OrderTracking was already created in 0001_initial; leave this migration empty to avoid
    # duplicate table errors when deploying fresh databases.
    operations = []
