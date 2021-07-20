# Update Analyze code for the future version of DELVE, containing the Bliss and Chou-Talalay methods

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math


class Analyze():

	def bliss(self, input_data):
            drug1_response = input_data[input_data['Drug2'] == '0.00000000']
            drug2_response = input_data[input_data['Drug1'] == 0]
            

            r1 = np.add.outer(drug1_response ['Effect'], drug2_response ['Effect'])
            r2 = np.multiply.outer(drug1_response ['Effect'], drug2_response ['Effect'])
            r3 = r1-r2
            pd.dataframe(r3)
            
            
#            pred_temp = []
#            for i in drug1_response['Effect']:
#                    i = float(i)
#                    temp =[]
#                    for j in drug2_response['Effect']:
 ##                      temp.append(i+j-i*j)
 #                       pred_temp.append(temp)  
 #                       pred_effect = np.array(pred_temp)
#                        
#            obs_temp = input_data['Effect']
#            obs_effect = np.array(obs_temp)
#            obs_effect = obs_effect.reshape(-1,6)
#            bliss_CI_score = obs_effect - pred_effect
#            
            return bliss_CI_score

###Orignal DELVE code Dylan worked on
'''            
#############################################################################   
#############################################################################

            drug1.response =
            drug2.response = 
            
            pred_effect = val1 + val2 - val1 * val2

pred = []
	for val2 in base2:
		val2 = float(val2)
		temp = []
		for val1 in base1:
			val1 = float(val1)
			temp.append(val1 + val2 - val1 * val2)
		pred.append(temp)

	# build observed matrix from dataframe
	# could use numpy functions to do this, but done here from scratch
	# faster and easier to understand what's going on
	obs = []
	for i in range(1, len(cols)):
		temp = []
		col = df1[cols[i]]
		for j in range(1, len(col)):
			temp.append(min(max(col[j], 0.001), 0.999))
		obs.append(temp)

	# build matrix of bliss scores
	bliss = []
	graph = []
	pos_count = 0
	for colnum in range(len(base1)):
		temp = []
		temp2 = []
		for rownum in range(len(base1)):
			observed = obs[colnum][rownum]
			predicted = pred[colnum][rownum]
			result = round(100 * (observed - predicted), 2)
			if result > 0:
				pos_count += 1
			tup = (result, str(result))
			temp.append(tup)
			temp2.append(result)

		bliss.append(temp)
		graph.append(temp2)


#############################################################################   
#############################################################################      
        
        
		return input_data

	def chou_talalay(self, input_data):
		# TO DO
        
#############################################################################   
#############################################################################       
 
        # chou talalay
	t1 = dose1
	t2 = dose2
	dose1 = dose1[1:]
	dose2 = dose2[1:]

	# Function to calculate the linear regression for the logarithmic form of the median-effect equation and medium effect dose
	def regress_and_med_dose_values(dose_lst, base_lst):
	    # Converting the list of doses and base cytotoxicity values to the logarithmic form.
	    log_D = np.array(np.log10(dose_lst))
	    log_f = np.array(np.log10([((y) / (1 - (y))) for y in base_lst]))

	    # Computation of the linear regression and medium dosage
	    slope, intercept, r_value, p_value, std_err = stats.linregress(log_D, log_f)
	    medium_dose = 10 ** (- intercept / (slope))

	    # Outputting a tuple of significant calculated values.
	    return(slope, std_err, intercept, r_value, medium_dose)

	# Function to calculate combination index each combination of drugs given their cytotoxic effects.
	def combination_index(medium_dose1, slope1, medium_dose2, slope2, f_affected, dose1, dose2):
	    return (((dose1 + dose2) * (dose1 / (dose1 + dose2))) / (medium_dose1 * (f_affected / (1 - f_affected)) ** (1 / slope1)) + ((dose1 + dose2) * (dose2 / (dose1 + dose2))) / (medium_dose2 * (f_affected / (1 - f_affected)) ** (1 / slope2)))

	  # Storing of medium effect dosages for different drugs
	med_dose1 = regress_and_med_dose_values(dose1, base1)[4]
	med_dose2 = regress_and_med_dose_values(dose2, base2)[4]

	  # Storing of the slope of the linear regression
	slope1 = regress_and_med_dose_values(dose1, base1)[0]
	slope2 = regress_and_med_dose_values(dose2, base2)[0]

	# Storing of r values for different drugs
	r1 = regress_and_med_dose_values(dose1, base1)[3]
	r2 = regress_and_med_dose_values(dose2, base2)[3]

	new_obs = map(list, zip(*obs))

	# Generation of Combination Index Matrix
	combo_index = []
	for colnum in range(len(base1)):
	    temp = []
	    for rownum in range(len(base1)):
	      observed = new_obs[colnum][rownum]
	      fstdose = dose2[rownum]
	      snddose = dose1[colnum]
	      result = round(combination_index(med_dose2, slope2, med_dose1, slope1, observed, fstdose, snddose), 4)
	      tup = (result, str(result))
	      temp.append(tup)
	    combo_index.append(temp)

	#combo_index = map(list, zip(*combo_index))

   
#############################################################################   
#############################################################################      

		return  input_data
'''
def read_data(filename):
	# Get the data from CSV file, name must be a string
	data_in = pd.read_csv(filename, index_col=0)
	# Now we transform the data an XYZ matrix into XYZ Column vectors:
	data_in = data_in.unstack().reset_index()
	data_in.columns=["Drug1","Drug2","Effect"]
	return data_in

def draw(dframes):
	# The draw function takes in a list of panda dataframes and plots each graph on the same plot
	# shape the canvas so it can fit all the plots
	fig = plt.figure(figsize=plt.figaspect(1/len(dframes)))

	# Loop through the list plotting each graph
	for frames in enumerate(dframes):
		ax = fig.add_subplot(1, len(dframes), frames[0]+1, projection='3d')
		df = frames[1]
		# This will plot the graph with a colour bar
		surf = ax.plot_trisurf(df['Drug1'], df['Drug2'], df['Effect'], cmap='viridis', linewidth=0.2)
		fig.colorbar(surf, shrink=0.5, aspect=8)

	plt.tight_layout()
	plt.show()


# ------------ Example Usage: ------------

# read data:
original = read_data("test2.csv")
# intiate analysis class

drug1_response = original[original['Drug2'] == '0.00000000']
drug2_response = original[original['Drug1'] == 0]

r1 = np.add.outer(drug1_response ['Effect'], drug2_response ['Effect'])
r2 = np.multiply.outer(drug1_response ['Effect'], drug2_response ['Effect'])
r3 = r1-r2


#Unfinished work
pd.DataFrame(np.transpose(r3)).stack()

np.reshape(r3,(1,))
pd.DataFrame(r3).stack()

r3

r4 = original['Effect'] - r3
#original["Bliss"] = original['Effect'] - r3[2]

#obs_temp = original['Effect']
#obs_effect = np.array(obs_temp)
#obs_effect = obs_effect.reshape(-1,6)
bliss_CI_score = original['Effect'] - r3

print(bliss_CI_score)

print(original)


print(drug1_response)

print(drug2_response)

Analyze = Analyze()

#calculate new datasets
bliss = Analyze.bliss(original)
print(bliss)
#chou_talalay = Analyze.chou_talalay(original)

# draw the graphs
#draw([original, bliss, chou_talalay])
