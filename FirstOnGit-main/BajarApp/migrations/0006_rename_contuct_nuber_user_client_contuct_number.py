# Generated by Django 4.2.5 on 2023-09-28 13:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BajarApp', '0005_product_category_alter_product_product_des_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_client',
            old_name='contuct_nuber',
            new_name='contuct_number',
        ),
    ]