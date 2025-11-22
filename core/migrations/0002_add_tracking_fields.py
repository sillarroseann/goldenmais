from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    # These fields already exist in the initial migration. Leave this migration as a no-op
    # so Django's migration history stays consistent without trying to add duplicate columns.
    operations = []
