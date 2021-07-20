# Calculation 
import time
import json
import numpy as np
import pandas as pd
from datetime import date

# Django
from itertools import chain
from django.db.models import Q
from django.urls import reverse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import Http404, HttpResponseRedirect, HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from django.views.generic.edit import FormMixin
from django.views.generic import DetailView, ListView, TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

# App specific
from delve import models
from helper import plot, tox_plot
from delve.forms import UserForm, CancerForm, DrugForm, RegistrationForm, TokenVerificationForm, CellLineForm

# Unique libs
from dal import autocomplete

# For twilio sms tfa
from django.conf import settings
from authy.api import AuthyApiClient
from .decorators import twofa_required


authy_api = AuthyApiClient(settings.ACCOUNT_SECURITY_API_KEY)


# ========================
# For Custom user model
# from django.contrib.auth import get_user_model
# User = get_user_model()
# ========================


# from django.views.decorators.csrf import csrf_exempt
# @csrf_exempt
# def sms(request):
# 	twiml = '<Response><Message>Hello from your Django app!</Message></Response>'
# 	return HttpResponse(twiml, content_type='text/xml')

class docs(LoginRequiredMixin, TemplateView):
	login_url = '/user_login/'
	redirect_field_name = 'redirect_to'
	template_name = 'delve/_documentation.html'
	
	def get(self, request, *args, **kwargs):
		
		def Average(lst): 
			return sum(lst) / len(lst) 
	
		mahta_combos = models.Combo.objects.filter(Q(Scientist__id=3))
		kelly_combos = models.Combo.objects.filter(Q(Scientist__id=5))
		shared_pairs = [[254, 459], [282, 396], [258, 434], [274, 409], [238, 453], [276, 403], [269, 393], [277, 402], [275, 410], [283, 398], [278, 413], [271, 406], [220, 466], [270, 392], [273, 400], [272, 401], [256, 435]]
		ic50_dif_lst = []
		print('part 1 done')
		
		whos_higher = 0
		# in pairs check differences of drugs
		for pair in shared_pairs:
			k = models.Ic50.objects.filter(experiment_id = pair[0])
			m = models.Ic50.objects.filter(experiment_id = pair[1])
			for ic50_k in k:
				for ic50_m in m:
					if ic50_m.drug1_id == ic50_k.drug1_id:
						dif = (ic50_m.effect - ic50_k.effect)
						
						if dif < 100 and dif > -100 :
							ic50_dif_lst.append(dif)
							if dif > 0:
								whos_higher += 1
						else:
							break
		print('part 3 done')
		# from 17 lists initially
		print('The final number of combos are:', len(ic50_dif_lst))

		print('mahta is higher in :', (whos_higher))
		
		print(Average(ic50_dif_lst))

		context = {'avg':Average(ic50_dif_lst), 'lst': ic50_dif_lst}
		return HttpResponse(context)

class indexView(TemplateView):
	template_name = 'delve/index.html'

class DashView(TemplateView, LoginRequiredMixin):
	login_url = '/user_login/'
	redirect_field_name = 'user_login'

	template_name = 'delve/dash.html'

	def get(self, request, *args, **kwargs):
		Combo = models.Combo.objects.all()
		# plot.leading_indication_for_drug()
		# plot.leading_combos_for_drug()
		
		# print(Combo[0].df_pickled))
		# for combo in Combo:
		# 		combo.CellLine, combo.Scientist, combo.drug_1, combo.drug_2 = combo.drug_1, combo.drug_2, combo.CellLine, combo.Scientist
		# 		combo.save()
		# 		combo.df_pickled = tox_plot.df_format(combo.df_pickled)
		# print(Combo[0].df_pickled)


		return render(request, self.template_name, {})

	def post(self, request, *args, **kwargs):
		return render(request, self.template_name, {})

class Ic50Search(TemplateView):
	# login_url = '/user_login/'
	# redirect_field_name = 'user_login'

	template_name = 'delve/ic50_search.html'

	def get(self, request, *args, **kwargs):
		Combo = models.Combo.objects.all()
		
		return render(request, self.template_name, {})

class cellLine_view(TemplateView, FormMixin,autocomplete.Select2QuerySetView):
	form_class = CellLineForm
	template_name = 'delve/cellLines.html'
		
	def get(self, request, *args, **kwargs):
		form = self.form_class(initial=self.initial)
		search_request = request.GET.get('cellLine_query')
		print("search_request is:",search_request)
		if search_request:
			reverse('cell-autocomplete')

		context = {
			"cellLines": models.Cellline.objects.all(),
			"form":form,
		}
		
		print(context)
		return render(request, self.template_name, context)

class CellAutoComplete(autocomplete.Select2QuerySetView):
	# Must return a list
	# by default self.q is the query of autocomplete
	def get_queryset(self):
		
		cellLines = models.Cellline.objects.all().filter(cell_line__istartswith=self.q)
		results =  cellLines
		return list(results)
		
# @login_required
class M2M_View(TemplateView):
	template_name = 'delve/ML_GV.html'

	def get(self, request, *args, **kwargs):
		runs_queryset = models.ML_Result.objects.all()
		print(runs_queryset)
		context = {
			'runs' : runs_queryset,
		}
		return render(request, self.template_name, context)

class upload(TemplateView, FormMixin):

	# form_class = DataSheet
	template_name = 'delve/report_index.html'
	
	def get(self, request, *args, **kwargs):
		form = self.form_class(initial=self.initial)
		return render(request, self.template_name, {'form': form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.FILES['drugFile'])
		excel_table = self.excel_table_list(request.FILES['drugFile'])  
		return render(request, self.template_name, {'drugFile': request.FILES['drugFile'], 'form': form, 'excel_table': excel_table})

		
	def excel_to_html(self, file):
		# Returns html table of excel
		df = pd.read_excel(file)
		return df.to_html()

	def excel_table_list(self, file):
		# Returns a list of html tables for each table generated in excel file
		
		df = pd.read_excel(file)
		# spits horizontialy
		df_list =  np.split(df, df[df.isnull().all(1)].index) 
		transposed_df_list = []
		for indexed_df in df_list:
			df1_transposed = indexed_df.T
			try:
				transposed_df_list.extend(np.split(df1_transposed, df1_transposed[df1_transposed.isnull().all(1)].index))
			except:
				transposed_df_list.extend([indexed_df])
		for tdf in transposed_df_list:
			tdf.dropna(how='all', inplace=True)
			tdf.dropna(how='all', inplace=True, axis=1)            
		
		for idx, indexed_df in enumerate(transposed_df_list):
			if np.prod(transposed_df_list[idx].shape) < np.prod(transposed_df_list[0].shape) and not indexed_df.empty:
				transposed_df_list[idx], transposed_df_list[0] = transposed_df_list[0], transposed_df_list[idx]

		html_table_list = []
		for single_df in transposed_df_list:
			single_df =  single_df.replace(np.nan, '', regex=True)
			if not single_df.empty:
				html_table_list.append(single_df.to_html(index=False))
		return html_table_list

class ada_upload(TemplateView, FormMixin):

	# form_class = DataSheet
	template_name = 'delve/ada_upload.html'
	
	def get(self, request, *args, **kwargs):
		form = self.form_class(initial=self.initial)
		return render(request, self.template_name, {'form': form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.FILES['drugFile'])
		excel_table = self.excel_table_list(request.FILES['drugFile'])  
		return render(request, self.template_name, {'drugFile': request.FILES['drugFile'], 'form': form, 'excel_table': excel_table})

		
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('user_login'))

def user_login(request):
	if request.method == 'POST':
		email = request.POST.get('email')
		password = request.POST.get('password')
		user = authenticate(username=email, password=password)
		if user:
			if user.is_active:
				login(request,user)
				return HttpResponseRedirect(reverse('index'))
			else:
				return HttpResponse("Your account was inactive.")
		else:
			print("Someone tried to login and failed.")
			return render(request, 'delve/login.html', {'message':'Invalid credentials', 'email':email})
	else:
		return render(request, 'delve/login.html', {})

class report_idx(TemplateView):
	template_name = 'delve/report_index.html'
	
	def get(self, request, *args, **kwargs):

		Combos = models.Combo.objects.all()
		paginator = Paginator(Combos, 15) # Show 25 combos per page
		page = request.GET.get('page')
		context = {
			'report_idx': paginator.get_page(page)
		}
		return render(request, self.template_name, context)
	


class drug_view(TemplateView, FormMixin, autocomplete.Select2QuerySetView):
	form_class = DrugForm

	# form_class = DataSheet
	template_name = 'delve/drugs.html'
	# template_name = 'sample_tests.html'

	def get(self, request, *args, **kwargs):

		#########
		start_time 		= time.time()
		elapsed_time 	= time.time() - start_time
		print(elapsed_time)
		#########
		
		# Autocomplete
		form = self.form_class(initial=self.initial)
		search_request = request.GET.get('drug_query')
		if search_request:
			reverse('ic50-autocomplete')

		context = {}
		page = request.GET.get('page')
	
		# Check if query matches cancer, drug, cellline, scietnist, or model
		# DRUG IS ONLY REQUIRED ARGUMENT IN QUERY
		# if form.is_valid():
		
		if request.GET.get('drugs'):
			#########
			elapsed_time = time.time() - start_time
			print(elapsed_time)
			#########
			drug_id = request.GET.get('drugs')
			try:
				query = models.Drug.objects.get(pk=drug_id)
			except:
				pass
				# query = models.Cellline.objects.get(pk=drug_id)
			context['welcome_message'] = "Query for drug: "+str(query)
			combos = models.Combo.objects.filter(Q(drug_1__drug_name=query.drug_name) | Q(drug_2__drug_name=query.drug_name) | Q(drug_2__code_name=query.code_name) | Q(drug_2__code_name=query.code_name))
			ic50s = []
				
##########################################################################################################################################################################################################################################
			# drugs_used = set() # set
			# ic50s_used = set()
			# cancers_used = set()
			# for combo in combos:
			# 	if combo.drug_2.id == query.id:
			# 		drugs_used.add(combo.drug_1.id)
			# 	else:
			# 		drugs_used.add(combo.drug_2.id)
			# 	ic50s_used.add(models.Ic50.objects.filter(experiment_id=combo.id))
			# 	cancers_used.add(combo.CellLine.indication)
			# elapsed_time = time.time() - start_time
			
			# #########
			# print(elapsed_time)
			# avg_score = {}
			# #########

			# for drug in drugs_used:
			# 	avg_score[drug.drug_name] = list()
			# 	for combo in combos:
			# 		if combo.drug_1 == drug or combo.drug_2 == drug:
			# 			avg_score[drug.drug_name].append(combo.Chou_score)


			# for key, values in avg_score.items():
			# 	avg_score[key] = sum(values)/len(values)
				
			# percent_score = {}
			# for key, values in avg_score.items():
			# 	percent_score[key] = avg_score[key]/(25)
########################################################################################################################################################################################################################			


			#########
			# Datum #
			#########
			# combo synergy score
			# ic50 score
			# num of 
			# variance of scores
			# t score of distribution of combo.score
			# WANT: low variance, high score, 90th percentile against other drugs
			# THINK ABOUT: Dosage range of interest

			##########################
			# Best performing combos #
			##########################
			
			context.update({
				'query': query.drug_name, 
				# 'test_chart': plot.t_distrib(),		
				# 'test_chart': plot.multi_y_bar_chart(),		
				'test_chart': plot.leading_drugs_w_avg(),		
				'leading_cellLine_for_drug': plot.leading_cellLine_for_drug(),		
				'leading_cellLine_for_combo': plot.leading_cellLine_for_combo(),	
				'leading_indication_for_drug': plot.leading_indication_for_drug(),	
				'leading_indication_for_combo': plot.leading_indication_for_combo(),	
				# 'test_chart': plot.multi_y_bar_chart(),		
				# 'efficay_chart': plot.histogram(avg_score, "# of Synergies when "+query.drug_name+" comboed with 2nd Drug"),		# Bar chart of synergistic scores with each drug
				# 'percentile_chart': plot.percentile_chart(avg_score, "# of Synergies when "+query.drug_name+" comboed with 2nd Drug"),		# (avg) ic50 chart of drug for each combo
				# 'concordance_chart': plot.concordance_chart(avg_score, "# of Synergies when "+query.drug_name+" comboed with 2nd Drug"),	#  
				# 'cancer_chart': plot.cancer_chart(avg_score, "# of Synergies when "+query.drug_name+" comboed with 2nd Drug"),			# 
				# 'cancer_percent_chart': plot.cancer_percent_chart(percent_score, "Percentage of dosage combinations with Synergy in Combo"),	# 
			 	# best perfrming combos
			})

		

		else:
			#Normal page load		
			ic50s = models.Ic50.objects.all()[:10]
			combos = models.Combo.objects.all()[:10]
			drug_info=models.Drug.objects.all()
			context['info']=drug_info
			context['welcome_message'] = "Most Recent"

		#########
		elapsed_time = time.time() - start_time
		print(elapsed_time)
		#########

		context.update({
			'form': form,
			'drug': models.Combo.objects.latest('id').drug_2,
			'ic50s': ic50s,
			'combos': Paginator(combos, 15).get_page(page),
			'leading_drugs_all_scores': plot.leading_drugs_all_scores(),		
			'leading_drugs_avg_chou': plot.leading_drugs_w_avg(),	
		})

	
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		context = {}
		return render(request, self.template_name, context)

class ic50_discrete_view(DetailView, TemplateView, FormMixin):
	pk_url_kwarg = 'id' 
	template_name = 'delve/ic50_page_selection.html'

	def get(self, request, combo_id, drug_id, **kwargs):
		combo = models.Combo.objects.get(id=combo_id)
		drug = models.Drug.objects.get(id=drug_id)
		if combo.drug_1.id == drug.id: 
			drug_2 = combo.drug_2
		else:
			drug_2 = combo.drug_1

		cellLine = models.Combo.objects.get(id=combo_id).CellLine
		cancer = cellLine.indication
		
		context = {
			'combo': combo,
			'drug':  drug, 
			'drug_2': drug_2,
			'cellLine':  cellLine,
			'Cancer': cancer,
			'ic50': plot.ic50_graph(combo.df_pickled), 
			# 'ic50': models.Ic50.objects.get(drug1_id=drug_id, experiment_id=combo_id),
		}
		return render(request, self.template_name, context)

class cancer_page_view(TemplateView, FormMixin, autocomplete.Select2QuerySetView):
	form_class = CancerForm
	template_name = 'delve/cancer_page.html'

	def get(self, request, *args, **kwargs):
		form = self.form_class(initial=self.initial)
		search_request = request.GET.get('cancer_query')
		if search_request:
			reverse('cancer-autocomplete')

		context = {
			"cancers": models.Cancer.objects.all(),
			"combos": models.Combo.objects.all(),
			"form": form,
		}
		return render(request, self.template_name, context)
	
	def post(self, request, *args, **kwargs):
		context = {}
		return render(request, self.template_name, context)


class cancer_detail_redirect(TemplateView):
	def get(self, request, cancer_id, *args, **kwargs):
		cancer = models.Cancer.objects.get(id=cancer_id)
		return HttpResponse(cancer.get_absolute_url())

class cancer_detail_view(TemplateView):
	template_name = 'delve/cancer_page_detail.html'


	def get(self, request, name, cancer_id, *args, **kwargs):
		context = {}
		try:
			cancer = models.Cancer.objects.get(id=cancer_id)
			context['cancer'] = cancer 

		except Exception as e:			
			print('error: ', e)	

		return render(request, self.template_name, context)

from django import template
register = template.Library()

@register.filter()
def as_table(model):
	ret = ""
	for name in model._meta.get_all_field_names():
		try:
			field = str(getattr(model, name))
			if field:
				ret += '<tr><td class="name">'+name+'</td><td class="field">'+field+'</td></td>'
		except AttributeError:
			pass
	return ret
class cancer_overview_view(TemplateView, FormMixin, autocomplete.Select2QuerySetView):
	form_class = CancerForm
	template_name = 'delve/cancer_page_overview.html'

	def get(self, request, *args, **kwargs):
		# cancer_schema = models.Cancer_Model_Form()
		model = models.Cancer
		field_names = [f.name for f in model._meta.get_fields()]
		print(field_names)
		data = [[getattr(ins, name) for name in field_names[1::]] for ins in  models.Cancer.objects.all()]
		
		return render(request, self.template_name, {'data': data, 'field_names':field_names })

	def post(self, request, *args, **kwargs):
		return render(request, self.template_name, {})



#TODO filter out results depending on the visitor
class CellLineAutoComplete(autocomplete.Select2QuerySetView):
	# Must return a list
	# by default self.q is the query of autocomplete
	def get_queryset(self):
		
		cellLines = models.Cellline.objects.all().filter(cell_line__istartswith=self.q)
		cancers = models.Cancer.objects.all().filter(cancer_name__istartswith=self.q)
		results = chain(cancers, cellLines)
		return list(results)

class DrugAndCellLineAutoComplete(autocomplete.Select2QuerySetView):
	# Must return a list
	# by default self.q is the query of autocomplete
	def get_queryset(self):
		
		cellLines = models.Cellline.objects.all().filter(cell_line__istartswith=self.q)
		drugs = models.Drug.objects.all().filter(drug_name__istartswith=self.q)
		drug_code = models.Drug.objects.all().filter(code_name__istartswith=self.q)
		results = chain(drugs, cellLines, drug_code)
		# results = drugs
		return list(results)

# move this

class NavAutoComplete(autocomplete.Select2QuerySetView):
	# Must return a list
	# by default self.q is the query of autocomplete
	def post(self, request, *args, **kwargs):
		return HttpResponse({'error':'nothing sent'}, content_type="application/json")

	def get(self, request, *args, **kwargs):
		response_data = {}
		try:
				
			searchRequest = list(request.GET.keys())[0].strip('][').replace('"','').split(',') 

			if searchRequest:
				cellLines = models.Cellline.objects.none()
				drugs = models.Drug.objects.none()
				cancers = models.Cancer.objects.none()

				for term in searchRequest:
					cellLines |= models.Cellline.objects.all().filter(cell_line__istartswith=term)
					drugs |= models.Drug.objects.all().filter(drug_name__istartswith=term)
					cancers |= models.Cancer.objects.all().filter(cancer_name__istartswith=term)
				# ic50s = models.Ic50.objects.all().filter(drug_name__istartswith=self.q)
				# try:
				# 	raise ValueError('A very specific bad thing happened.')
				# 	all_objects =  [*cellLines, *drugs, *cancers]
				# 	data = serializers.serialize('json', all_objects)
				# 	print('serialized')
				# except:
				response_data = {
					'cell lines': list(cellLines.values('cell_line', 'indication', 'accession_number')),
					'drugs': list(drugs.values('drug_name')),
					'cancers': list(cancers.values('cancer_name')),
				}
		except Exception as e:
			response_data = {'error':'nothing sent'}
			
		return HttpResponse(json.dumps(response_data), content_type="application/json")

class quickData(LoginRequiredMixin, TemplateView, autocomplete.Select2QuerySetView):
	login_url = '/user_login/'
	redirect_field_name = 'redirect_to'
	template_name = 'delve/quickData.html'

	def get(self, request, *args, **kwargs):
		search_request = request.GET.get('cancer_query')
		if search_request:
			reverse('cancer-autocomplete')

		context = {
			"cancers": models.Cancer.objects.all(),
			"combos": models.Combo.objects.all(),
		}
		exc = models.Combo.objects.filter(id=1)
		print(exc[0].drug_1)
		print(exc[0].drug_1.id)
		print(exc[0].get_df().iloc[:1])
		print(exc[0].drug_2)
		print(exc[0].drug_2.id)
		print(exc[0].get_df().iloc[:, 0:1].T)
		# leading_ic50s_for_drug()

		return render(request, self.template_name, context)
	
	def post(self, request, *args, **kwargs):
		context = {}
		return render(request, self.template_name, context)
		
class automation_page_select_view(LoginRequiredMixin, TemplateView):
	login_url = '/user_login/'
	redirect_field_name = 'redirect_to'
	template_name = 'delve/automation_page_select.html'

	def get(self, request, *args, **kwargs):
		context = {}

		return render(request, self.template_name, context)
	
	def post(self, request, *args, **kwargs):
		context = {}
		return render(request, self.template_name, context)

class automation_page_ticket_table_view(LoginRequiredMixin, TemplateView):
	login_url = '/user_login/'
	redirect_field_name = 'redirect_to'
	template_name = 'delve/automation_page_ticket_table.html'

	def get(self, request, *args, **kwargs):
		context = {}

		return render(request, self.template_name, context)
	
	def post(self, request, *args, **kwargs):
		context = {}
		return render(request, self.template_name, context)

# ============================================================================
# 2FA (twilio/authy)
# ============================================================================
def TwoFA_home(request):
	return render(request, 'twofa/home.html')


def TwoFA_register(request):
	if not request.user.is_anonymous:
		return redirect('dash')
	if request.method == 'POST':
		print('registering')
		form = RegistrationForm(request.POST)
		if form.is_valid():
			print('form is valid')
			authy_user = authy_api.users.create(
				form.cleaned_data['email'],
				form.cleaned_data['phone_number'],
				form.cleaned_data['country_code'],
			)
			if authy_user.ok():
				print('user is ok')
				twofa_user = models.Profile.objects.create_user(
					form.cleaned_data['email'],
					form.cleaned_data['first_name'],
					form.cleaned_data['last_name'],
					authy_user.id,
					form.cleaned_data['password']
				)
				login(request, twofa_user)
				return redirect('twilio_2fa')
			else:
				print('user is not ok')
				for key, value in authy_user.errors().items():
					form.add_error(
						None,
						'{key}: {value}'.format(key=key, value=value)
					)
					print('{key}: {value}'.format(key=key, value=value))
		else:
			print('form is not valid')
			print(form.errors)
	else:
		form = RegistrationForm()
	return render(request, 'twofa/register.html', {'form': form})


@login_required
def TwoFA_twofa(request):
	if request.method == 'POST':
		form = TokenVerificationForm(request.POST)
		if form.is_valid(request.user.authy_id):
			request.session['authy'] = True
			return redirect('dash')
	else:
		form = TokenVerificationForm()
	return render(request, 'twofa/2fa.html', {'form': form})


@login_required
def TwoFA_token_sms(request):
	sms = authy_api.users.request_sms(request.user.authy_id, {'force': True})
	if sms.ok():
		return HttpResponse('SMS request successful', status=200)
	else:
		return HttpResponse('SMS request failed', status=503)


@login_required
def TwoFA_token_voice(request):
	call = authy_api.users.request_call(request.user.authy_id, {'force': True})
	if call.ok():
		return HttpResponse('Call request successfull', status=200)
	else:
		return HttpResponse('Call request failed', status=503)


@login_required
def TwoFA_token_onetouch(request):
	details = {
		'Authy ID': request.user.authy_id,
		'Username': request.user.username,
		'Reason': 'Demo by Account Security'
	}

	hidden_details = {
		'test': 'This is a'
	}

	response = authy_api.one_touch.send_request(
		int(request.user.authy_id),
		message='Login requested for Account Security account.',
		seconds_to_expire=120,
		details=details,
		hidden_details=hidden_details
	)
	if response.ok():
		request.session['onetouch_uuid'] = response.get_uuid()
		return HttpResponse('OneTouch request successfull', status=200)
	else:
		return HttpResponse('OneTouch request failed', status=503)


@login_required
def TwoFA_onetouch_status(request):
	uuid = request.session['onetouch_uuid']
	approval_status = authy_api.one_touch.get_approval_status(uuid)
	if approval_status.ok():
		if approval_status['approval_request']['status'] == 'approved':
			request.session['authy'] = True
		return HttpResponse(
			approval_status['approval_request']['status'],
			status=200
		)
	else:
		return HttpResponse(approval_status.errros(), status=503)


@twofa_required
def TwoFA_protected(request):
	return render(request, 'delve/dash.html')

def page_404(request):
	return render(request, 'delve/404.html')

def is_authenticated(request):
	return HttpResponse(json.dumps(request.user.is_authenticated), status=200)
