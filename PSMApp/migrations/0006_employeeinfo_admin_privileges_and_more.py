# Generated by Django 4.2 on 2025-01-23 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PSMApp', '0005_productinfo_unit_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeinfo',
            name='admin_privileges',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='settlementinfo',
            name='settlement_method',
            field=models.CharField(choices=[('cash', '現金決済'), ('card', 'カード決済')], default='cash', max_length=10, verbose_name='決済方法'),
        ),
    ]
