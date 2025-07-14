from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_ban_level_alter_user_ban_until_and_more'),  # <-- твоя последняя миграция
    ]

    operations = [
        migrations.RenameField(
            model_name='loginattempt',
            old_name='ts',
            new_name='created_at',
        ),
    ]

