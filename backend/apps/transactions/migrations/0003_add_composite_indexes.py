from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_add_constraints'),  # ← исправьте на вашу последнюю миграцию
    ]

    operations = [
        migrations.AddIndex(
            model_name='transaction',
            index=models.Index(fields=['budget', '-date'], name='idx_budget_date'),
        ),
        migrations.AddIndex(
            model_name='transaction',
            index=models.Index(fields=['budget', 'category'], name='idx_budget_category'),
        ),
        migrations.AddIndex(
            model_name='transaction',
            index=models.Index(fields=['type'], name='idx_trans_type'),
        ),
        migrations.AddIndex(
            model_name='transaction',
            index=models.Index(fields=['budget', 'type'], name='idx_budget_type'),
        ),
    ]