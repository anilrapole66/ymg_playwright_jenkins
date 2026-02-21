from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("employees", "0006_leaveapplication"),
    ]

    operations = [
        migrations.AddField(
            model_name="employee",
            name="employee_serial_id",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
