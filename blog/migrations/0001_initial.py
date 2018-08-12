# Generated by Django 2.0.7 on 2018-08-12 20:07

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('remember_token', models.CharField(blank=True, max_length=100, null=True)),
                ('role_id', models.IntegerField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='County',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='FormAll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_entered', models.DateField(blank=True, null=True)),
                ('date_needed', models.DateField(blank=True, null=True)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('client', models.CharField(blank=True, max_length=200, null=True)),
                ('project_no', models.CharField(blank=True, max_length=200, null=True)),
                ('map_no', models.CharField(blank=True, max_length=50, null=True)),
                ('contact', models.CharField(blank=True, max_length=50, null=True)),
                ('phone', models.CharField(blank=True, max_length=50, null=True)),
                ('notes', models.CharField(blank=True, max_length=500, null=True)),
                ('certify_to', models.CharField(blank=True, max_length=200, null=True)),
                ('lender', models.CharField(blank=True, max_length=200, null=True)),
                ('gf_no', models.CharField(blank=True, max_length=50, null=True)),
                ('address_street', models.CharField(blank=True, max_length=200, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('state', models.CharField(blank=True, max_length=50, null=True)),
                ('zipcode', models.CharField(blank=True, max_length=50, null=True)),
                ('country', models.CharField(blank=True, max_length=50, null=True)),
                ('survey_type', models.CharField(blank=True, max_length=10, null=True)),
                ('county', models.CharField(blank=True, max_length=50, null=True)),
                ('subdivision', models.CharField(blank=True, max_length=200, null=True)),
                ('unit', models.CharField(blank=True, max_length=50, null=True)),
                ('sub_block', models.CharField(blank=True, max_length=50, null=True)),
                ('lot', models.CharField(blank=True, max_length=50, null=True)),
                ('survey', models.CharField(blank=True, max_length=200, null=True)),
                ('rural_block', models.CharField(blank=True, max_length=50, null=True)),
                ('rural_section', models.CharField(blank=True, max_length=50, null=True)),
                ('meridian', models.CharField(blank=True, max_length=10, null=True)),
                ('t_r', models.CharField(blank=True, max_length=10, null=True)),
                ('plss_section', models.CharField(blank=True, max_length=50, null=True)),
                ('folder_path', models.CharField(blank=True, max_length=300, null=True)),
                ('prad_acct', models.CharField(blank=True, max_length=50, null=True)),
                ('prad_acct_gis', models.CharField(blank=True, max_length=50, null=True)),
                ('clerksfile', models.CharField(blank=True, max_length=50, null=True)),
                ('book', models.CharField(blank=True, max_length=50, null=True)),
                ('page', models.CharField(blank=True, max_length=50, null=True)),
                ('surveyor', models.CharField(blank=True, max_length=50, null=True)),
                ('filed', models.CharField(blank=True, max_length=50, null=True)),
                ('cancelled', models.CharField(blank=True, max_length=50, null=True)),
                ('user_id', models.IntegerField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('requested_by', models.CharField(blank=True, max_length=255, null=True)),
                ('well_name', models.CharField(blank=True, max_length=255, null=True)),
                ('well_number', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'form_all',
            },
        ),
        migrations.CreateModel(
            name='FormAllCanadian',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_entered', models.DateField(blank=True, null=True)),
                ('date_needed', models.DateField(blank=True, null=True)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('client', models.CharField(blank=True, max_length=200, null=True)),
                ('project_no', models.CharField(blank=True, max_length=200, null=True)),
                ('map_no', models.CharField(blank=True, max_length=50, null=True)),
                ('contact', models.CharField(blank=True, max_length=50, null=True)),
                ('phone', models.CharField(blank=True, max_length=50, null=True)),
                ('notes', models.CharField(blank=True, max_length=500, null=True)),
                ('certify_to', models.CharField(blank=True, max_length=200, null=True)),
                ('lender', models.CharField(blank=True, max_length=200, null=True)),
                ('gf_no', models.CharField(blank=True, max_length=50, null=True)),
                ('address_street', models.CharField(blank=True, max_length=200, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('state', models.CharField(blank=True, max_length=50, null=True)),
                ('zipcode', models.CharField(blank=True, max_length=50, null=True)),
                ('country', models.CharField(blank=True, max_length=50, null=True)),
                ('survey_type', models.CharField(blank=True, max_length=10, null=True)),
                ('county', models.CharField(blank=True, max_length=50, null=True)),
                ('subdivision', models.CharField(blank=True, max_length=200, null=True)),
                ('unit', models.CharField(blank=True, max_length=50, null=True)),
                ('sub_block', models.CharField(blank=True, max_length=50, null=True)),
                ('lot', models.CharField(blank=True, max_length=50, null=True)),
                ('survey', models.CharField(blank=True, max_length=200, null=True)),
                ('rural_block', models.CharField(blank=True, max_length=50, null=True)),
                ('rural_section', models.CharField(blank=True, max_length=50, null=True)),
                ('meridian', models.CharField(blank=True, max_length=10, null=True)),
                ('t_r', models.CharField(blank=True, max_length=10, null=True)),
                ('plss_section', models.CharField(blank=True, max_length=50, null=True)),
                ('folder_path', models.CharField(blank=True, max_length=300, null=True)),
                ('prad_acct', models.CharField(blank=True, max_length=50, null=True)),
                ('prad_acct_gis', models.CharField(blank=True, max_length=50, null=True)),
                ('clerksfile', models.CharField(blank=True, max_length=50, null=True)),
                ('book', models.CharField(blank=True, max_length=50, null=True)),
                ('page', models.CharField(blank=True, max_length=50, null=True)),
                ('surveyor', models.CharField(blank=True, max_length=50, null=True)),
                ('filed', models.CharField(blank=True, max_length=50, null=True)),
                ('cancelled', models.CharField(blank=True, max_length=50, null=True)),
                ('user_id', models.IntegerField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('requested_by', models.CharField(blank=True, max_length=255, null=True)),
                ('well_name', models.CharField(blank=True, max_length=255, null=True)),
                ('well_number', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'form_all_canadian',
            },
        ),
        migrations.CreateModel(
            name='FormAllFurman',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_entered', models.DateField(blank=True, null=True)),
                ('date_needed', models.DateField(blank=True, null=True)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('client', models.CharField(blank=True, max_length=200, null=True)),
                ('project_no', models.CharField(blank=True, max_length=200, null=True)),
                ('map_no', models.CharField(blank=True, max_length=50, null=True)),
                ('contact', models.CharField(blank=True, max_length=50, null=True)),
                ('phone', models.CharField(blank=True, max_length=50, null=True)),
                ('notes', models.CharField(blank=True, max_length=500, null=True)),
                ('certify_to', models.CharField(blank=True, max_length=200, null=True)),
                ('lender', models.CharField(blank=True, max_length=200, null=True)),
                ('gf_no', models.CharField(blank=True, max_length=50, null=True)),
                ('address_street', models.CharField(blank=True, max_length=200, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('state', models.CharField(blank=True, max_length=50, null=True)),
                ('zipcode', models.CharField(blank=True, max_length=50, null=True)),
                ('country', models.CharField(blank=True, max_length=50, null=True)),
                ('survey_type', models.CharField(blank=True, max_length=10, null=True)),
                ('county', models.CharField(blank=True, max_length=50, null=True)),
                ('subdivision', models.CharField(blank=True, max_length=200, null=True)),
                ('unit', models.CharField(blank=True, max_length=50, null=True)),
                ('sub_block', models.CharField(blank=True, max_length=50, null=True)),
                ('lot', models.CharField(blank=True, max_length=50, null=True)),
                ('survey', models.CharField(blank=True, max_length=200, null=True)),
                ('rural_block', models.CharField(blank=True, max_length=50, null=True)),
                ('rural_section', models.CharField(blank=True, max_length=50, null=True)),
                ('meridian', models.CharField(blank=True, max_length=10, null=True)),
                ('t_r', models.CharField(blank=True, max_length=10, null=True)),
                ('plss_section', models.CharField(blank=True, max_length=50, null=True)),
                ('folder_path', models.CharField(blank=True, max_length=300, null=True)),
                ('prad_acct', models.CharField(blank=True, max_length=50, null=True)),
                ('prad_acct_gis', models.CharField(blank=True, max_length=50, null=True)),
                ('clerksfile', models.CharField(blank=True, max_length=50, null=True)),
                ('book', models.CharField(blank=True, max_length=50, null=True)),
                ('page', models.CharField(blank=True, max_length=50, null=True)),
                ('surveyor', models.CharField(blank=True, max_length=50, null=True)),
                ('filed', models.CharField(blank=True, max_length=50, null=True)),
                ('cancelled', models.CharField(blank=True, max_length=50, null=True)),
                ('user_id', models.IntegerField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('requested_by', models.CharField(blank=True, max_length=255, null=True)),
                ('well_name', models.CharField(blank=True, max_length=255, null=True)),
                ('well_number', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'form_all_furman',
            },
        ),
        migrations.CreateModel(
            name='MasterGeom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', models.TextField(blank=True, null=True)),
                ('mtrs', models.CharField(blank=True, max_length=20, null=True)),
                ('meridian', models.CharField(blank=True, max_length=10, null=True)),
                ('township', models.CharField(blank=True, max_length=10, null=True)),
                ('field_range', models.CharField(blank=True, db_column='_range', max_length=10, null=True)),
                ('section', models.CharField(blank=True, max_length=10, null=True)),
                ('t_r', models.CharField(blank=True, max_length=10, null=True)),
                ('county', models.CharField(blank=True, max_length=50, null=True)),
                ('anum', models.CharField(blank=True, max_length=12, null=True)),
                ('l1surnam', models.CharField(blank=True, max_length=32, null=True)),
                ('l2block', models.CharField(blank=True, max_length=10, null=True)),
                ('l3surnum', models.CharField(blank=True, max_length=8, null=True)),
                ('duplicat', models.CharField(blank=True, max_length=1, null=True)),
                ('state', models.CharField(blank=True, max_length=10, null=True)),
                ('join_type', models.CharField(blank=True, max_length=50, null=True)),
                ('join_field', models.CharField(blank=True, max_length=200, null=True)),
                ('account_nu', models.CharField(blank=True, max_length=20, null=True)),
                ('parcel_num', models.CharField(blank=True, max_length=10, null=True)),
                ('map_number', models.CharField(blank=True, max_length=20, null=True)),
                ('lot_number', models.CharField(blank=True, max_length=20, null=True)),
                ('block_numb', models.CharField(blank=True, max_length=10, null=True)),
                ('subdivisio', models.CharField(blank=True, max_length=50, null=True)),
                ('unit_numbe', models.CharField(blank=True, max_length=10, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('parcel_cou', models.CharField(blank=True, max_length=10, null=True)),
                ('parcel_typ', models.CharField(blank=True, max_length=10, null=True)),
                ('street', models.CharField(blank=True, max_length=50, null=True)),
                ('street_pfx', models.CharField(blank=True, max_length=2, null=True)),
                ('street_sfx', models.CharField(blank=True, max_length=10, null=True)),
                ('zip', models.CharField(blank=True, max_length=10, null=True)),
                ('city', models.CharField(blank=True, max_length=25, null=True)),
                ('globalid', models.CharField(blank=True, max_length=38, null=True)),
                ('edit_date', models.DateField(blank=True, null=True)),
                ('edit_by', models.CharField(blank=True, max_length=50, null=True)),
                ('shape_leng', models.CharField(blank=True, max_length=255, null=True)),
                ('shape_area', models.CharField(blank=True, max_length=255, null=True)),
                ('county_code', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'master_geom',
            },
        ),
    ]
