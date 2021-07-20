# Generated by Django 2.2.4 on 2020-12-17 06:00

from django.db import migrations, models
import django.db.models.deletion
import picklefield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cancer',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('unnamed_0', models.BigIntegerField(blank=True, db_column='Unnamed: 0', null=True)),
                ('index', models.BigIntegerField(blank=True, null=True)),
                ('cancer_type', models.TextField(blank=True, null=True)),
                ('cancer_name', models.TextField(blank=True, null=True)),
                ('cancer_class', models.TextField(blank=True, null=True)),
                ('number_2017_incidence', models.TextField(blank=True, db_column='2017_incidence', null=True)),
                ('number_2018_incidence', models.TextField(blank=True, db_column='2018_incidence', null=True)),
                ('unnamed_5', models.FloatField(blank=True, db_column='unnamed:_5', null=True)),
                ('notes_2018', models.TextField(blank=True, null=True)),
                ('rare_for_6_100_000_r_nr_19_682', models.TextField(blank=True, db_column='rare_for_<6/100,000?_r/nr_<19,682', null=True)),
                ('rare_for_15_100_000_r_nr_49_205', models.TextField(blank=True, db_column='rare_for_<15/100,000?_r/nr_<49,205', null=True)),
                ('number_2017_prevalence', models.TextField(blank=True, db_column='2017_prevalence', null=True)),
                ('number_2015_prevalence_15_112_098', models.FloatField(blank=True, db_column='2015_prevalence_15,112,098', null=True)),
                ('number_2015_prevalence_nr_only', models.FloatField(blank=True, db_column='2015_prevalence_nr_only', null=True)),
                ('orphan_200_000_prevalence_y_n', models.FloatField(blank=True, db_column='orphan_<200,000_prevalence_y/n', null=True)),
                ('number_2017_mortality', models.TextField(blank=True, db_column='2017_mortality', null=True)),
                ('pediatric_field', models.TextField(blank=True, db_column='pediatric?', null=True)),
                ('pediatric_incidence_most_recenlty_available', models.TextField(blank=True, null=True)),
                ('women_field', models.TextField(blank=True, db_column='women?', null=True)),
                ('minority_field', models.TextField(blank=True, db_column='minority?', null=True)),
                ('number_5_year_survival_rates', models.TextField(blank=True, db_column='5-year_survival_rates', null=True)),
                ('median_survival_time', models.TextField(blank=True, null=True)),
                ('approved_therapies_y_n', models.TextField(blank=True, db_column='approved_therapies_y/n', null=True)),
                ('targeted_therapy_drugs', models.TextField(blank=True, null=True)),
                ('description_notes', models.TextField(blank=True, db_column='description/notes', null=True)),
                ('chemo', models.TextField(blank=True, null=True)),
                ('comparison', models.TextField(blank=True, null=True)),
                ('primary_data_sources', models.TextField(blank=True, null=True)),
                ('other_date_sources', models.TextField(blank=True, null=True)),
                ('verfiefied_by_field', models.FloatField(blank=True, db_column='verfiefied_by...', null=True)),
                ('field_all_data_not_cited_is_from_american_cancer_society_and_seer_field', models.FloatField(blank=True, db_column='*_all_data_not_cited_is_from_american_cancer_society_and_seer,_', null=True)),
                ('stage_i_5yr_survival_rate', models.FloatField(blank=True, null=True)),
                ('stage_ii_5yr_survival_rate', models.FloatField(blank=True, null=True)),
                ('stage_iii_5yr_survival_rate', models.FloatField(blank=True, null=True)),
                ('stage_iv_5yr_survival_rate', models.FloatField(blank=True, null=True)),
                ('unnamed_33', models.FloatField(blank=True, db_column='unnamed:_33', null=True)),
                ('unnamed_34', models.FloatField(blank=True, db_column='unnamed:_34', null=True)),
                ('unnamed_35', models.FloatField(blank=True, db_column='unnamed:_35', null=True)),
                ('unnamed_36', models.TextField(blank=True, db_column='unnamed:_36', null=True)),
                ('not_found_or_mentioned_by_name_or_corresponding_in_the_aacr_a', models.FloatField(blank=True, db_column='not_found,_or_mentioned_by_name_or_corresponding,_in_the_aacr_a', null=True)),
                ('gen', models.FloatField(blank=True, null=True)),
                ('children_bool', models.BooleanField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Cancer',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Cellline',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False, unique=True)),
                ('cell_line', models.TextField(blank=True, db_column='Cell Line', null=True)),
                ('in_culture', models.TextField(blank=True, db_column='In Culture', null=True)),
                ('number_2d_cell_well', models.TextField(blank=True, db_column='2D Cell / Well', null=True)),
                ('doubling_time', models.FloatField(blank=True, db_column='Doubling time', null=True)),
                ('rare_non_rare', models.TextField(blank=True, db_column='Rare / Non Rare', null=True)),
                ('rna_seq_data_field', models.BigIntegerField(blank=True, db_column='RNA Seq data?', null=True)),
                ('link', models.TextField(blank=True, db_column='Link', null=True)),
                ('accession_number', models.TextField(blank=True, db_column='Accession Number', null=True)),
                ('source', models.TextField(blank=True, db_column='Source', null=True)),
                ('license', models.FloatField(blank=True, db_column='License', null=True)),
                ('passage', models.FloatField(blank=True, db_column='Passage', null=True)),
                ('current_owner', models.TextField(blank=True, db_column='Current Owner', null=True)),
                ('flask', models.TextField(blank=True, db_column='Flask', null=True)),
                ('density', models.TextField(blank=True, db_column='Density', null=True)),
                ('models', models.TextField(blank=True, db_column='Models', null=True)),
            ],
            options={
                'db_table': 'cellLine',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Drug',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('drug_name', models.TextField(blank=True, null=True)),
                ('cid', models.FloatField(blank=True, db_column='Cid', null=True)),
                ('iupac_name', models.TextField(blank=True, db_column='IUPAC_name', null=True)),
                ('canonicalsmiles', models.TextField(blank=True, db_column='CanonicalSmiles', null=True)),
                ('isomericsmiles', models.TextField(blank=True, db_column='IsomericSmiles', null=True)),
                ('synonyms', models.TextField(blank=True, db_column='Synonyms', null=True)),
                ('half_life', models.TextField(blank=True, db_column='Half_life', null=True)),
                ('code_name', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'drug',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Scientists',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('scientist_id', models.BigIntegerField(blank=True, db_column='Scientist_id', null=True, unique=True)),
                ('scientist_name', models.CharField(blank=True, db_column='Scientist_name', max_length=150, null=True)),
            ],
            options={
                'db_table': 'scientists',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Combo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='def.', max_length=150, null=True)),
                ('image', models.ImageField(default='combo_photos/default.png', upload_to='combo_photos/previews/')),
                ('Synergies', models.IntegerField(default=None, null=True)),
                ('Ic50', models.CharField(default=None, max_length=150, null=True)),
                ('df_pickled', picklefield.fields.PickledObjectField(default=1, editable=False)),
                ('void', models.BooleanField(db_column='Void')),
                ('HSA_score', models.IntegerField(default=None, null=True)),
                ('Loewe_score', models.IntegerField(default=None, null=True)),
                ('Bliss_score', models.IntegerField(default=None, null=True)),
                ('ZIP_score', models.IntegerField(default=None, null=True)),
                ('Chou_score', models.IntegerField(default=None, null=True)),
                ('CellLine', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='delve.Cellline')),
                ('Scientist', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='delve.Scientists')),
                ('drug_1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='drug_1', to='delve.Drug')),
                ('drug_2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='drug_2', to='delve.Drug')),
            ],
            options={
                'db_table': 'Combo',
            },
        ),
        migrations.CreateModel(
            name='delveTasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('1', 'page'), ('2', 'delve'), ('3', 'todo')], max_length=9, null=True)),
                ('details', models.CharField(default=None, max_length=150, null=True)),
                ('status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Ic50',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('effect', models.FloatField(blank=True, null=True)),
                ('drug1_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='delve.Drug')),
                ('experiment_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='delve.Combo')),
            ],
            options={
                'db_table': 'Ic50',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('image', models.ImageField(default='default.jpg', upload_to='profile_pics')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('phone_number_verified', models.BooleanField(default=False)),
                ('change_pw', models.BooleanField(default=True)),
                ('authy_id', models.CharField(blank=True, max_length=12, null=True)),
                ('country_code', models.IntegerField(default=1)),
                ('two_factor_auth', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'Profiles',
            },
        ),
    ]
