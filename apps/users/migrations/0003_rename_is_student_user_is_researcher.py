from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_subscription_plan_type_alter_user_tier'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_student',
            new_name='is_researcher',
        ),
    ]
