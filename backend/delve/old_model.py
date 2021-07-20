from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
import psycopg2

def opencon1():
	con = psycopg2.connect(
	            dbname="dea9bjtdgcvdps",
	            user="uba50q29lce6b3",
	            password="p6a0292746b6c66a9360c5d91811ccbb849311ee51b2c33317c5f45ef6e956340",
	            host="ec2-18-211-71-159.compute-1.amazonaws.com",
	            port="5432"
	            )
	cur = con.cursor()
	return(con, cur)

def retrieveAll():
	con, cur = opencon1()
	cur.execute("""SELECT DISTINCT drug1, drug2, cell_line, scientist, experiment_name, concl_exists FROM combos""")
	combos = cur.fetchall()
	con.close()
	return combos

def get_tox():
	con, cur = opencon1()
	cur.execute("""SELECT DISTINCT drug1, drug2, tox, cell_line, scientist, experiment_name, concl_exists FROM combos""")
	combos = cur.fetchall()
	con.close()
	return combos

def getdrug():
	return db_select(select=["drug_id", "drug_name"], _from=["drugs"])

''' --------------------- Custom SQL request code ------------------------- ''' 
###I didn't like the built in django ORM - from my understand it was not suited towards the goal here
### Below I have written my own abstracted database retrivial functions

# Open the connection to the Postgre Database
def opencon2():
	con = psycopg2.connect(
	            dbname="test1",
	            user="shepherd",
	            password="shepherd",
	            host="127.0.0.1",
	            port="5432"
	            )
	cur = con.cursor()
	return(con, cur)

# This function delists the inputs to the sql query functions
def lstr(ls, sep=', '): 
	return sep.join(map(str, ls))


# These are the sql query funcitons, the connection is opened, the input is checked for type, and the database
# is queried with the constructed string, the connection is then closed. 

def db_insert(insert:list=None, into:list=None, values:list=None):
	con, cur = opencon2()
	query = 'INSERT INTO '+lstr(into)+' ('+lstr(insert)+') VALUES ('+lstr(values)+')'
	con.commit(query)
	con.close()
	cur.close()

def db_select(select:list = None, _from:list = None, where:list = None):
	con, cur = opencon2()
	if (select == None) or (_from == None):
		raise Exception("SELECT or FROM not specified")
	elif where == None: 
		query = 'SELECT '+lstr(select)+' FROM '+lstr(_from)
	else:
		query = 'SELECT '+lstr(select)+' FROM '+lstr(_from)+' WHERE '+lstr(where, " AND ")
	cur.execute(query)
	rows = cur.fetchall()
	con.close()
	cur.close()
	return rows

def db_sql(query:str, select=False):
	con, cur = opencon2()
	if select:
		cur.execute(query)
		rows = cur.fetchall()
		con.close()
		cur.close()
		return rows
	else:
		con.commit(query)

### Below are the database models for interacting with forms.py

# class CellLine(models.Model):
#     cell_line_id = models.BigAutoField(primary_key=True)
#     cell_line_name = models.TextField(blank=True, null=True)
#     source_company = models.TextField(blank=True, null=True)
#     source_url = models.TextField(blank=True, null=True)
#     license = models.TextField(blank=True, null=True)
#     species = models.TextField(blank=True, null=True)
#     tissue_type = models.TextField(blank=True, null=True)
#     media_type = models.TextField(blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'cell_line'
#     def __str__(self):
#     	return self.cell_line_name

# class Combo(models.Model):
#     combo_id = models.BigAutoField(primary_key=True)
#     experiment_id = models.BigIntegerField(blank=True, null=True)
#     assay_type = models.TextField(blank=True, null=True)
#     drug1_id = models.BigIntegerField(blank=True, null=True)
#     drug2_id = models.BigIntegerField(blank=True, null=True)
#     drug1_conc = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
#     drug2_conc = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
#     effect = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
#     notes = models.TextField(blank=True, null=True)
#     bliss = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
#     chou_talalay = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
#     processed_by = models.TextField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'combo'

# class Drugs(models.Model):
#     drug_id = models.BigAutoField(primary_key=True)
#     drug_name = models.TextField(blank=True, null=True)
#     code_name = models.TextField(blank=True, null=True)
#     smile = models.TextField(blank=True, null=True)
#     iupac_name = models.TextField(blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'drugs'
#     def __str__(self):
#     	return self.drug_name 

# class ExpBundle(models.Model):
#     bundle_id = models.BigAutoField(primary_key=True)
#     bundle_name = models.TextField(blank=True, null=True)
#     info = models.TextField(blank=True, null=True)
#     bundle_date = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'exp_bundle'

# class Experiment(models.Model):
#     experiment_id = models.BigAutoField(primary_key=True)
#     session_id = models.TextField(blank=True, null=True)
#     exp_type = models.TextField(blank=True, null=True)
#     upload_user_id = models.TextField(blank=True, null=True)
#     scientist_id = models.TextField(blank=True, null=True)
#     cell_line_id = models.BigIntegerField(blank=True, null=True)
#     indication_id = models.TextField(blank=True, null=True)
#     upload_date = models.DateTimeField(blank=True, null=True)
#     equipment_info = ArrayField(models.TextField(blank=True, null=True))  # This field type is a guess.
#     notes = models.TextField(blank=True, null=True)
#     delve_version = models.BigIntegerField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'experiment'

# class ExperimentEditHistory(models.Model):
#     edit_id = models.BigAutoField(primary_key=True)
#     experiment_id = models.TextField(blank=True, null=True)
#     user_id = models.TextField(blank=True, null=True)
#     edit_note = models.TextField(blank=True, null=True)
#     edit_date = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'experiment_edit_history'

# class Ic50(models.Model):
#     ic50_id = models.BigAutoField(primary_key=True)
#     experiment_id = models.BigIntegerField(blank=True, null=True)
#     drug1_id = models.BigIntegerField(blank=True, null=True)
#     drug1_conc = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
#     effect = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
#     processed_by = models.TextField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'ic50'

# class Indication(models.Model):
#     indication_id = models.BigAutoField(primary_key=True)
#     indication_name = models.TextField(blank=True, null=True)
#     indicidence = models.BigIntegerField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'indication'

# class Users(models.Model):
#     user_id = models.BigAutoField(primary_key=True)
#     user_name = models.TextField(blank=True, null=True)
#     email = models.TextField(blank=True, null=True)
#     password = models.TextField(blank=True, null=True)
#     user_type = models.TextField(blank=True, null=True)
#     first_name = models.TextField(blank=True, null=True)
#     last_name = models.TextField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'users'        