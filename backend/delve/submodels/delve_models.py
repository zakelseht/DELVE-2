import os
import psycopg2
import time



from django.contrib.postgres.fields import ArrayField
from django.template.defaultfilters import slugify
from django.urls import reverse, reverse_lazy
from django.forms import ModelForm 
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from helper import tox_plot
import pandas as pd
from picklefield.fields import PickledObjectField

# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 52428800
# 100MB 104857600
# 250MB - 214958080
# 500MB - 429916160
MAX_UPLOAD_SIZE = "5242880" 

class MyProfileManager(BaseUserManager):
    class params:
        db = 'default'

    def create_user(self, email, first_name, last_name, authy_id, password=None):
        if not email:
            raise ValueError("Users must have an email")
        if not first_name:
            raise ValueError("Users must have a first name")
        if not last_name:
            raise ValueError("Users must have a last name")
        if not authy_id:
            raise ValueError("Users must have a phone number")

        user = self.model(
            email = self.normalize_email(email),
            authy_id=authy_id,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
    
        return user

    def create_superuser(self, email, first_name, last_name, authy_id, password):
        
        user = self.create_user(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            authy_id = authy_id,
            password = password,
        )

        user.is_admin       = True
        user.is_superuser   = True
        user.is_staff       = True

        user.save(using=self._db)
        return user      


class Profile(AbstractBaseUser, PermissionsMixin):
    class params:
        db = 'default'
    # user                        = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Custom 
    image                       = models.ImageField(default='default.jpg', upload_to='profile_pics')
    date_joined                 = models.DateTimeField(verbose_name='date joined', auto_now_add = True) 
    last_login                  = models.DateTimeField(verbose_name='last login', auto_now = True)
    # Required
    email                       = models.EmailField(verbose_name = 'email', max_length = 60, unique = True)
    first_name                  = models.CharField(max_length = 30, unique = False)
    last_name                   = models.CharField(max_length = 30, unique = False)
    is_admin                    = models.BooleanField(default = False)
    is_active                   = models.BooleanField(default = True)
    is_staff                    = models.BooleanField(default = False)
    is_superuser                = models.BooleanField(default = False)
    # Adding
    phone_number_verified       = models.BooleanField(default=False)
    change_pw                   = models.BooleanField(default=True)
    authy_id                    = models.CharField(max_length=12, null=True, blank=True)
    country_code                = models.IntegerField(default=1)
    two_factor_auth             = models.BooleanField(default=False)

    USERNAME_FIELD              = 'email'
    EMAIL_FIELD                 = 'email'
    REQUIRED_FIELDS             = ['first_name','last_name', 'authy_id']

    objects = MyProfileManager() 
    
    class Meta:
        db_table = 'Profiles'

    def __str__(self):
        return self.last_name + ", " + self.first_name
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True




class Cancer(models.Model):
    class params:
        db = 'default'

    id = models.BigIntegerField(primary_key=True)
    unnamed_0 = models.BigIntegerField(db_column='Unnamed: 0', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    index = models.BigIntegerField(blank=True, null=True)
    cancer_type = models.TextField(blank=True, null=True)
    cancer_name = models.TextField(blank=True, null=True)
    cancer_class = models.TextField(blank=True, null=True)
    number_2017_incidence = models.TextField(db_column='2017_incidence', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_2018_incidence = models.TextField(db_column='2018_incidence', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    unnamed_5 = models.FloatField(db_column='unnamed:_5', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    notes_2018 = models.TextField(blank=True, null=True)
    rare_for_6_100_000_r_nr_19_682 = models.TextField(db_column='rare_for_<6/100,000?_r/nr_<19,682', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    rare_for_15_100_000_r_nr_49_205 = models.TextField(db_column='rare_for_<15/100,000?_r/nr_<49,205', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    number_2017_prevalence = models.TextField(db_column='2017_prevalence', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_2015_prevalence_15_112_098 = models.FloatField(db_column='2015_prevalence_15,112,098', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it wasn't a valid Python identifier.
    number_2015_prevalence_nr_only = models.FloatField(db_column='2015_prevalence_nr_only', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    orphan_200_000_prevalence_y_n = models.FloatField(db_column='orphan_<200,000_prevalence_y/n', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    number_2017_mortality = models.TextField(db_column='2017_mortality', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    pediatric_field = models.TextField(db_column='pediatric?', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    pediatric_incidence_most_recenlty_available = models.TextField(blank=True, null=True)
    women_field = models.TextField(db_column='women?', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    minority_field = models.TextField(db_column='minority?', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    number_5_year_survival_rates = models.TextField(db_column='5-year_survival_rates', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it wasn't a valid Python identifier.
    median_survival_time = models.TextField(blank=True, null=True)
    approved_therapies_y_n = models.TextField(db_column='approved_therapies_y/n', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    targeted_therapy_drugs = models.TextField(blank=True, null=True)
    description_notes = models.TextField(db_column='description/notes', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    chemo = models.TextField(blank=True, null=True)
    comparison = models.TextField(blank=True, null=True)
    primary_data_sources = models.TextField(blank=True, null=True)
    other_date_sources = models.TextField(blank=True, null=True)
    verfiefied_by_field = models.FloatField(db_column='verfiefied_by...', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    field_all_data_not_cited_is_from_american_cancer_society_and_seer_field = models.FloatField(db_column='*_all_data_not_cited_is_from_american_cancer_society_and_seer,_', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'.
    stage_i_5yr_survival_rate = models.FloatField(blank=True, null=True)
    stage_ii_5yr_survival_rate = models.FloatField(blank=True, null=True)
    stage_iii_5yr_survival_rate = models.FloatField(blank=True, null=True)
    stage_iv_5yr_survival_rate = models.FloatField(blank=True, null=True)
    unnamed_33 = models.FloatField(db_column='unnamed:_33', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    unnamed_34 = models.FloatField(db_column='unnamed:_34', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    unnamed_35 = models.FloatField(db_column='unnamed:_35', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    unnamed_36 = models.TextField(db_column='unnamed:_36', blank=True, null=True)   # Field renamed to remove unsuitable characters.
    not_found_or_mentioned_by_name_or_corresponding_in_the_aacr_a = models.FloatField(db_column='not_found,_or_mentioned_by_name_or_corresponding,_in_the_aacr_a', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    gen = models.FloatField(blank=True, null=True)
    children_bool = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Cancer'

    def get_absolute_url(self):
        return reverse('cancer-detail', kwargs={'name':self.cancer_name, 'cancer_id':self.id})

    def __str__(self):
        return str(self.cancer_type+"-->"+self.cancer_name)

class Cancer_Model_Form(ModelForm):
    class Meta:
        model = Cancer
        fields = '__all__'

class Cellline(models.Model):
    class params:
        db = 'default'


    id = models.BigIntegerField(primary_key = True, unique=True)
    cell_line = models.TextField(db_column='Cell Line', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    indication = models.ForeignKey("Cancer", on_delete=models.CASCADE, db_column='Indication', blank=True, null=True)  # Field name made lowercase.
    in_culture = models.TextField(db_column='In Culture', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    number_2d_cell_well = models.TextField(db_column='2D Cell / Well', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it wasn't a valid Python identifier.
    doubling_time = models.FloatField(db_column='Doubling time', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rare_non_rare = models.TextField(db_column='Rare / Non Rare', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rna_seq_data_field = models.BigIntegerField(db_column='RNA Seq data?', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    link = models.TextField(db_column='Link', blank=True, null=True)  # Field name made lowercase.
    accession_number = models.TextField(db_column='Accession Number', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    source = models.TextField(db_column='Source', blank=True, null=True)  # Field name made lowercase.
    license = models.FloatField(db_column='License', blank=True, null=True)  # Field name made lowercase.
    passage = models.FloatField(db_column='Passage', blank=True, null=True)  # Field name made lowercase.
    current_owner = models.TextField(db_column='Current Owner', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    flask = models.TextField(db_column='Flask', blank=True, null=True)  # Field name made lowercase.
    density = models.TextField(db_column='Density', blank=True, null=True)  # Field name made lowercase.
    models = models.TextField(db_column='Models', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cellLine'
        
    def __str__(self):
        return self.cell_line

class Drug(models.Model):
    class params:
        db = 'default'


    id = models.BigIntegerField(primary_key=True)
    drug_name = models.TextField(blank=True, null=True)
    cid = models.FloatField(db_column='Cid', blank=True, null=True)  # Field name made lowercase.
    iupac_name = models.TextField(db_column='IUPAC_name', blank=True, null=True)  # Field name made lowercase.
    canonicalsmiles = models.TextField(db_column='CanonicalSmiles', blank=True, null=True)  # Field name made lowercase.
    isomericsmiles = models.TextField(db_column='IsomericSmiles', blank=True, null=True)  # Field name made lowercase.
    synonyms = models.TextField(db_column='Synonyms', blank=True, null=True)  # Field name made lowercase.
    half_life = models.TextField(db_column='Half_life', blank=True, null=True)  # Field name made lowercase.
    code_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'drug'

    def __str__(self):
        if(self.code_name):
            return str(self.code_name+" ("+self.drug_name+')')
        else:
            return self.drug_name
    
    def get_code_name(self):
        if self.code_name:
            return self.code_name
        else:
            return self.drug_name


class Scientists(models.Model):
    class params:
        db = 'default'


    id = models.BigIntegerField(primary_key=True)
    scientist_id = models.BigIntegerField(db_column='Scientist_id', unique=True, blank=True, null=True)  # Field name made lowercase.
    scientist_name = models.CharField(max_length=150,db_column='Scientist_name', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'scientists'

    def __str__(self):
        return self.scientist_name


def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)

class Combo(models.Model):
    class params:
        db = 'default'


    name = models.CharField(max_length=150, null=True, default="def.")
    image = models.ImageField(default='combo_photos/default.png', upload_to='combo_photos/previews/')

    # Quantitative
    Synergies = models.IntegerField(default=None, null=True)
    Ic50 = models.CharField(default=None, max_length=150, null=True)    
    df_pickled = PickledObjectField(default = 1)
    void = models.BooleanField(db_column='Void')  # Field name made lowercase.

    # Synergy Scores
    HSA_score = models.IntegerField(default=None, null=True)
    Loewe_score = models.IntegerField(default=None, null=True)
    Bliss_score = models.IntegerField(default=None, null=True)
    ZIP_score = models.IntegerField(default=None, null=True)
    Chou_score = models.IntegerField(default=None, null=True)
    # HSA_score, Loewe_score, Bliss_score, ZIP_score, Chou_score

    # Qualitative
    drug_1 = models.ForeignKey('Drug', on_delete=models.CASCADE, related_name='drug_1', null=True)
    drug_2 = models.ForeignKey('Drug', on_delete=models.CASCADE, related_name='drug_2', null=True)
    CellLine = models.ForeignKey('Cellline', on_delete=models.CASCADE, null=True)
    Scientist = models.ForeignKey('Scientists', on_delete=models.CASCADE, null=True)


    # Preview_img = models.ImageField(upload_to='photos/', blank=True, null=True, max_length=5242880)
    class Meta:   
        db_table = 'Combo'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        # self.name = slugify(str(self.Scientist.scientist_name)+'-'+str(self.id))
        return reverse("Report", args=[self.id])
    
    def get_name(self):
        return slugify(str(self.name)+"-"+str(self.id))
    
    def get_df(self):
        # df = self.df_pickled
        # df = df.apply(pd.to_numeric)
        # df = (pd.DataFrame(df.to_dict()))
        # df = df.reindex(sorted(df.columns), axis=1)
        # df = (df.sort_index())
        # return df
        return tox_plot.df_format(self.df_pickled)

    def generate_conclusion(self, chou, bliss, both, r1, r2):
        return ("""Conclusion: Experiment %s examines the Combination of %s and %s on %s. 
            The Combo yielded %d synergistic values using the Chou-Talalay method and %d synergistic values using the Bliss Independence 
            model. %d points were found to be synergistic in both models. The r value for %s was %s, 
            and the r value for %s was %s."""% (self.name, self.drug_1, self.drug_2, self.CellLine, chou, bliss, both, self.drug_1, r1, self.drug_2, r2))

    def has_add_permission(self, request):
        return False
    
    def update_true_pickle(self):
        self.true_pickle = pd.read_json(self.df_pickled, orient='index', convert_axes=False)
        return
    

class Ic50(models.Model):
    class params:
        db = 'default'
        
    id = models.BigAutoField(primary_key=True)
    experiment_id = models.ForeignKey('Combo', on_delete=models.CASCADE, null=True)
    drug1_id = models.ForeignKey('Drug', on_delete=models.CASCADE, null=True)
    effect = models.FloatField(blank=True, null=True)
    class Meta:
        db_table = 'Ic50'
    def __str__(self):
        return self.ic50_id


class delveTasks(models.Model):
    class params:
        db = 'default'
        
    category = models.CharField(max_length=9, choices=[('1','page'), ('2','delve'), ('3','todo')], null=True) 
    details = models.CharField(default=None, max_length=150, null=True)
    status = models.BooleanField(default=False)