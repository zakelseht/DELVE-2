# Standard 
import pandas as pd
import numpy as np
# Built-ins
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from django.contrib import messages
from delve_site.settings import WKHTMLTOPDF_CONFIG

# Class-based views
from django.views.generic import DetailView, ListView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin

# Local
from ada.forms import Upload_Form
from delve import models
from . import plots
from helper import plot, tox_plot
from django.template.loader import get_template

# extra
import pdfkit
import pickle
import ast
from base64 import b64decode, b64encode




class upload(LoginRequiredMixin, TemplateView, FormMixin):
	login_url = '/user_login/'
	redirect_field_name = 'user_login'
	# form_class = Upload_Form
	template_name = 'delve/upload.html'
	
	def get(self, request, *args, **kwargs):
		return render(request, self.template_name, {})

	
	def post(self, request, *args, **kwargs):
		post_dict = {}
		# print(request.POST.dict())
# ============================================================================================================================================================================================================================
		if 'experiment_data' in request.FILES:
			print('Stage 1')
			post_dict['progress']='50'
			post_dict['stage']='1'

			data_file = request.FILES['experiment_data']
			extension = str(data_file).split(".")[1].lower()


			if extension.endswith('xlsx'):
				uncleaned_df = pd.read_excel(data_file, header=None)
			
			elif extension.endswith('csv'):
				uncleaned_df = pd.read_csv(data_file, header=None)
			# Reduce >=2 rows to 2    
			# uncleaned_df.dropna(how='all', inplace=True) 
			# uncleaned_df.dropna(how='all', inplace=True, axis=1) 
			uncleaned_df = uncleaned_df.fillna("")

			post_dict['sheet']=uncleaned_df.to_html(table_id='selectable', header=False, index=False)

			# else:
			# 	messages.error(request, 'Invalid File') 
			# 	return redirect('upload')

			# df_lst, html_table = self.df_to_list_to_html_lst(uncleaned_df) 
			# print(html_table)
	

			# request.session['excel_table'] = html_table
			# post_dict['excel_table'] = html_table

			# post_dict.update({
			# 	'experiment_data': request.FILES['experiment_data'], 
			# 	# 'form': self.form_class, 
			# 	'table_idx' : 1,
			# 	'excel_table' : request.session['excel_table'],
			# 	})



# ============================================================================================================================================================================================================================
		elif 'generate_report' in request.POST:
			post_dict['stage']='2'
			
			messages.Error(request, 'Post error occured') 
		
# ============================================================================================================================================================================================================================
		elif 'approve' in request.POST:
			post_dict['stage']='3'
			
			post_dict.update({
				'excel_table': request.session['excel_table'], 
				'form': self.form_class , 
				'table_idx' : int(request.POST['selected_table']),
				})			
			for idx, html_instance in enumerate(request.session['excel_table']):
				if idx == int(request.POST['selected_table']):
					df = pd.read_html(html_instance)


# ============================================================================================================================================================================================================================
		elif 'generate_report' in request.POST:	
			post_dict['stage']='4'
			
			for idx, html_instance in enumerate(request.session['excel_table']):
				if idx == int(request.POST['table_idx'])-1:
					df = pd.read_html(html_instance)[0]

					# Process df
					cleaned_df = self.processed_df(df)
					report_id = request.session['report_id']

					report = get_object_or_404(models.Combo, id=report_id)
					report.df_pickled=cleaned_df
					report.save()
					return redirect('Report', id=report_id)


		return render(request, self.template_name, post_dict)
# ============================================================================================================================================================================================================================
# ==============         END OF POST         ============================================================================================================================================================================================================
# ============================================================================================================================================================================================================================


	# def processed_df(self, df, starting_axis=1):
	# 	# Recursion based clean of data	
	# 	for idx, cell in enumerate(df.iloc[0].tolist()):
	# 		if idx == 0:
	# 			pass
	# 		if not cell:
	# 			df = df.drop(df.index[0]).reset_index(drop=True)
	# 			for idx, cell in enumerate(df[df.columns[0]].tolist()):
	# 				if not cell:
	# 					df = self.processed_df(df.drop(df.columns[0], axis=1)).reset_index(drop=True)
	# 					break
	# 			break

	# 	for idx, cell in enumerate(df[df.columns[0]].tolist()):
	# 		if idx == 0:
	# 			pass
	# 		if not cell:
	# 			df = self.processed_df(df.drop(df.columns[0], axis=1)).reset_index(drop=True)
	# 			break
		
	# 	return df

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

class report_page(DetailView, LoginRequiredMixin, TemplateView, FormMixin):
	
	login_url = '/user_login/'
	redirect_field_name = 'user_login'
	template_name = 'delve/CI_report.html'
	pk_url_kwarg = 'id'

	def get(self, request, *args, **kwargs):			
		### Display Selected Report ###
		report = get_object_or_404(models.Combo, id=self.kwargs['id'])
		print(report.df_pickled )
		df = report.df_pickled

		# Quick maths
		# dose1, dose2, base_cyto1, base_cyto2, obs_matrix, pred_matrix, viability1, viability2 = tox_plot.df_components(df)
		CI, bliss, doses1, doses2, med_dose1, med_dose2, r_val1, r_val2, slope1, slope2 = tox_plot.chou_talalay(df)


		report_data_dict = {
			# Strings
			'report':report,
			'conclusion':report.generate_conclusion(1,2,3,round(r_val1, 3),round(r_val2, 3)), #chou, bliss, both, r1, r2
			# Stats
			'med_dose1': round(med_dose1, 3),
			'r_val1': round(r_val1, 3),
			'slope1': round(slope1, 3),

			'med_dose2': round(med_dose2, 3),
			'r_val2': round(r_val2, 3),		
			'slope2': round(slope2, 3),

			# Lists
			'dose1': list(doses1.round(4)),
			'dose2': list(doses2.round(4)),
			# 'dose11': doses1[1:],

			# Tables 
			'citos': list(zip(doses1, df.round(3).values)),
			'CI': list(zip(doses1[1:], CI.round(3))),
			'bliss': list(zip(doses1[1:], bliss.round(3).astype(str))),
			
			# Graphs
			'3d_plot': (plot.API_Synergy(report.id)),
		}

		report.Processed = True
		report.save()

		if 'Download' in request.GET:



			template = get_template('delve/CI_report.html')	
			report_data_dict['pic']=True
			html  = template.render(report_data_dict)
			options = {
				'page-size': 'Letter',
				'encoding': "UTF-8",
			}
			# pdf = pdfkit.from_string(html, False, options, configuration=config)
			pdf = pdfkit.from_string(html, False, configuration = WKHTMLTOPDF_CONFIG, options = options)
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'attachment; filename = pperson_list_pdf.pdf'
			return response
			
		return render(request, self.template_name, report_data_dict)



	def post(self, request, *args, **kwargs):
		report = get_object_or_404(models.Combo, id=self.kwargs['id'])
		if 'upload' in request.POST:
			report.Processed = True
		return render(request, self.template_name)
	
	def head(self, request):
		print("Succeful Submission!!!!!")
		messages.success(request, 'Report status updated!')
		return render(request, self.template_name)	
	