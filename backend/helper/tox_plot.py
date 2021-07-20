import pandas as pd 
import numpy as np
from scipy import stats

import matplotlib
import matplotlib.pyplot as plt

def is_number(n):
	try:
		num = float(n)
		return True
	except ValueError:
		return False
def df_format(df):
	# THIS RUNS ONCE; IN THE INITIAL INPUT OF DATA
	# df[0].iloc[0] = 0 # special case to deal with chrom bio csv formating
	df = df.apply(pd.to_numeric)
	# df = (df.clip(lower=0.000001)).div(100)
	df = (pd.DataFrame(df.to_dict()))
	df = df.reindex(sorted(df.columns), axis=1)
	df = (df.sort_index())
	# print(df)
	return df


def df_components(df, optional_variable_1=None):
	#takes df_pickled element from combo model
	df = df_format(df)
	dose1 =	np.clip(np.array(df.index.tolist()).astype(float), 0.000001, None)
	dose2 = np.clip(np.array(df.columns.tolist()).astype(float), 0.000001, None)
	base_cyto1 = df[df.columns[0]].tolist()
	base_cyto2 = df.iloc[0].tolist()
	obs_matrix = df.values
	pred_matrix = [[(val1 + val2 - val1 * val2) for val1 in df.iloc[0]] for val2 in df[df.columns[0]]]
	viability1 = [((y) / (1 - (y))) for y in base_cyto1]
	viability2 = [((y) / (1 - (y))) for y in base_cyto2]
	return dose1, dose2, base_cyto1, base_cyto2, obs_matrix, pred_matrix, viability1, viability2

def regress_and_med_dose_values(dose_lst, base_lst):
# Function to calculate the linear regression for the logarithmic form of the median-effect equation and medium effect dose
	# Converting the list of doses and base cytotoxicity values to the logarithmic form.
	log_D = np.array(np.log10(dose_lst))
	log_f = np.array(np.log10([((y) / (1 - (y))) for y in base_lst]))
	# Computation of the linear regression and medium dosage
	slope, intercept, r_value, _p_value, std_err = stats.linregress(log_D, log_f)
	medium_dose = 10 ** (- intercept / (slope ))
	return(slope, std_err, intercept, r_value, medium_dose)

def combination_index(medium_dose1, slope1, medium_dose2, slope2, f_affected, dose1, dose2):
	result =  dose1 / (medium_dose1 * (f_affected / (1 - f_affected)) ** (1 / slope1)) + dose2 / (medium_dose2 * (f_affected / (1 - f_affected)) ** (1 / slope2))
	return(result)

def chou_talalay(df1):
		
	dose1, dose2, base_cyto1, base_cyto2, obs, pred, _, _ = df_components(df1)
	# Function to calculate combination index each combination of drugs given their cytotoxic effects.

	# Storing of medium effect dosages for different drugs
	slope1,_,_,r_val1,med_dose1 = regress_and_med_dose_values(dose1[1:], base_cyto1[1:])
	slope2,_,_,r_val2,med_dose2 = regress_and_med_dose_values(dose2[1:], base_cyto2[1:])

	# Generation of Combination Index Matrix
	combo_index = [[combination_index(med_dose1, slope1, med_dose2, slope2, obs[rownum][colnum], dose1[rownum], dose2[colnum]) for colnum in range(1,len(dose1))] for rownum in range(1,len(dose1))]
	bliss = [[100 * (obs[colnum][rownum] - pred[colnum][rownum]) for rownum in range(1,len(dose1))] for colnum in range(1,len(dose1))]
	print(bliss)
	return  np.array(combo_index), np.array(bliss), np.array(dose1), np.array(dose2), med_dose1, med_dose2, r_val1, r_val2, slope1, slope2

def bliss(df):

	dose1, _, _, _, obs, pred, _, _= df_components(df)
	bliss = [[100 * (obs[colnum][rownum] - pred[colnum][rownum]) for rownum in range(1,len(dose1))] for colnum in range(1,len(dose1))]

	return np.array(bliss)




# ====================================================================================================================================================================================================
# ====================================================================================================================================================================================================
# ====================================================================================================================================================================================================



def chou_score(df1):
		
	dose1, dose2, base_cyto1, base_cyto2, obs, _, _, _ = df_components(df1)
	slope1,_,_,_,med_dose1 = regress_and_med_dose_values(dose1[1:], base_cyto1[1:])
	slope2,_,_,_,med_dose2 = regress_and_med_dose_values(dose2[1:], base_cyto2[1:])

	combo_index = [[combination_index(med_dose1, slope1, med_dose2, slope2, obs[rownum][colnum], dose1[rownum], dose2[colnum]) for colnum in range(1,len(dose1))] for rownum in range(1,len(dose1))]


	score = 0
	flat = np.array(combo_index).flatten()
	# For chou if CI < 1 synergy, CI > 1 antagonism, CI = 1 additive
	for val in flat:
		if val < 1:
			score += 1	
	return score
	# return  np.array(combo_index)

def bliss_score(df):
	
	dose1, _, _, _, obs, pred, _, _= df_components(df)
	bliss = [[100 * (obs[colnum][rownum] - pred[colnum][rownum]) for rownum in range(1,len(dose1))] for colnum in range(1,len(dose1))]
	

	score = 0
	flat = np.array(bliss).flatten()
	# Synergistic if 
	for val in flat:
		if val < 1:
			score += 1	
	return score
	# return np.array(bliss)

def zip_score(df):
	
	dose1, _, _, _, obs, pred, _, _= df_components(df)
	zip_val = [[100 * (obs[colnum][rownum] - pred[colnum][rownum]) for rownum in range(1,len(dose1))] for colnum in range(1,len(dose1))]

	score = 0
	flat = np.array(zip_val).flatten()
	for val in flat:
		if val < 1:
			score += 1	
	return score
	# return np.array(zip)

def loewe_score(df):
	
	dose1, _, _, _, obs, pred, _, _= df_components(df)
	loewe = [[100 * (obs[colnum][rownum] - pred[colnum][rownum]) for rownum in range(1,len(dose1))] for colnum in range(1,len(dose1))]

	score = 0
	flat = np.array(loewe).flatten()
	# synergy of obs > loewe
	for val in flat:
		if val < 1:
			score += 1	
	return score
	# return np.array(loewe)

def hsa_score(df):
	
	dose1, _, _, _, obs, pred, _, _= df_components(df)
	hsa = [[max(obs[colnum][rownum], pred[colnum][rownum]) for rownum in range(1,len(dose1))] for colnum in range(1,len(dose1))]

	score = 0
	flat = np.array(hsa).flatten()
	# Synergy is observed > hsa otherwise not
	for val in flat:
		if val < 1:
			score += 1	
	return score
	# return np.array(hsa )



# TODO for MMRS scores --> Sigmoid function to normalize all 









class process():

	def __init__(self, df):
		self.df = df

	def processed_df(self, df):
			# Recursion based clean of data	
		for idx, cell in enumerate(df.iloc[0].tolist()):
			if idx == 0:
				pass
			if not is_number(cell):
				df = df.drop(df.index[0]).reset_index(drop=True)
				for idx, cell in enumerate(df[df.columns[0]].tolist()):
					if not is_number(cell):
						df = self.processed_df(df.drop(df.columns[0])).reset_index(drop=True)
						break
				break

		for idx, cell in enumerate(df[df.columns[0]].tolist()):
			if idx == 0:
				pass
			if not is_number(cell):
				df = self.processed_df(df.drop(df.columns[0])).reset_index(drop=True)
				break
		
		return df

	def df_list_to_html(self, df_list):
		html_table_list = []
		searchfor = ['cyto', 'inhib']
		for idx, single_df in enumerate(df_list):
			html_table_list.append(single_df.to_html(index=False, header=False))

		return html_table_list	

	def df_to_list_to_html_lst(self, df):
		# RETURNS 1) Processed data in list of parsed df's (Formated) and 2) the a list of the df's in html format 
		
		# Split 
		horizontally_split_df_list =  np.split(df, df[df.isnull().all(axis=1)].index) 
		df_list = []
		for indexed_df in horizontally_split_df_list:
			try:
				df_list.extend(np.split(indexed_df, indexed_df.columns[indexed_df.isnull().all()], axis=1))
			except:
				df_list.extend([indexed_df])

		# Drop empty rows and col
		for tdf in df_list:
			tdf.dropna(how='all', inplace=True)
			tdf.dropna(how='all', inplace=True, axis=1)            
		
		# df lists empty cells to 0's
		output_df_list = []
		for single_df in df_list:
			single_df =  single_df.replace(np.nan, 0, regex=True)
			
			if not single_df.empty:
				output_df_list.append(single_df)

		# to html formatted list
		html_table_list = []
		searchfor = ['cyto', 'inhib']
		for idx, single_df in enumerate(output_df_list):
			html_table_list.append(single_df.to_html(index=False, header=False))

		return output_df_list, html_table_list

def phil_ic50():
	# x(c,t)=e**(k*t(1-(Sm*c**h)/(SC50+c**h)-t(Kc*c**h)/(LC50**h+c**h)))
	return