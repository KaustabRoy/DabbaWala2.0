# Generated by Django 4.1.7 on 2023-11-23 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dabbawala', '0021_subcategory_parent_cat'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='item_sub_cat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dabbawala.subcategory'),
        ),
    ]
