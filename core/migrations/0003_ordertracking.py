from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_add_tracking_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderTracking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Order Placed'), ('confirmed', 'Order Confirmed'), ('processing', 'Preparing Order'), ('ready_for_pickup', 'Ready for Pickup'), ('shipped', 'Out for Delivery'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled')], max_length=20)),
                ('message', models.TextField()),
                ('location', models.CharField(blank=True, max_length=200)),
                ('updated_by', models.CharField(default='System', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tracking_updates', to='core.order')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
