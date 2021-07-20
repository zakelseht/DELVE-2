# Calculation
import json
import numpy as np
import requests
import pandas as pd
# Django
from itertools import chain
from django.db.models import Q
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, JsonResponse
from django.template.loader import render_to_string

# class based views
from django.views.generic import TemplateView, FormView

# App specific
from delve import models
from helper import plot, tox_plot, AWS_helper
# Unique libs
from dal import autocomplete
import inspect

# move this
from django.core import serializers
class GlobalNavSearchOptions(TemplateView):
	def get(self, request, *args, **kwargs):
		cell_lines = (list(models.Cellline.objects.values_list('cell_line',flat=True)))
		cancers = (list(models.Cancer.objects.values_list('cancer_name',flat=True)))
		drugs = (list(models.Drug.objects.values_list('drug_name',flat=True)))
		lst = list(chain(drugs, cancers, cell_lines))
		return HttpResponse(json.dumps(lst), content_type="application/json")

class testRestFramework(TemplateView):
	def get(self, request, *args, **kwargs):
		context = {}
		return render(request, self.template_name, context)
		
	def post(self, request, *args, **kwargs):
		context = {}
		return render(request, self.template_name, context)


from django.core import serializers


class GlobalNavSearchOptions(TemplateView):
	def get(self, request, *args, **kwargs):
		cell_lines = (
			list(models.Cellline.objects.values_list('cell_line', flat=True)))
		cancers = (
			list(models.Cancer.objects.values_list('cancer_name', flat=True)))
		drugs = (list(models.Drug.objects.values_list('drug_name', flat=True)))
		lst = list(chain(drugs, cancers, cell_lines))
		return HttpResponse(json.dumps(lst), content_type="application/json")


class testRestFramework(TemplateView):
	def get(self, request, *args, **kwargs):
		context = {}
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		context = {}
		return render(request, self.template_name, context)


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
		return HttpResponse({'error': 'nothing sent'}, content_type="application/json")

	def get(self, request, *args, **kwargs):
		try:
			searchRequest = list(request.GET.keys())[0].strip(
				'][').replace('"', '').split(',')

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

			return HttpResponse(json.dumps(response_data), content_type="application/json")
		except:
			pass

		return HttpResponse({'error': 'nothing sent'}, content_type="application/json")

		return HttpResponse(json.dumps(data), content_type="application/json")
	
	def post(self, request, *args, **kwargs):
		# change render to helper graphs
		graphicRequested = request.POST.get('graphicButton.val()')
		html = render_to_string('frontend/scroll.html', {'dishes': dishes})
		return HttpResponse(html)

class SMILESRequest(TemplateView):
	# slug_url_kwarg = 'the_slug'

	def get(self, request, *args, **kwargs):
		data = {}
		data['smilesList'] = list(models.Drug.objects.all().values_list('canonicalsmiles', flat=True))
		data['drugList'] = list(models.Drug.objects.all().values_list('drug_name', flat=True))
		return HttpResponse(json.dumps(data), content_type="application/json")

class quickData(TemplateView, autocomplete.Select2QuerySetView):
	template_name = 'delve/quickData.html'

	def get(self, request, *args, **kwargs):
		search_request = request.GET.get('cancer_query')
		if search_request:
			reverse('cancer-autocomplete')

		context = {
			"cancers": models.Cancer.objects.all(),
			"combos": models.Combo.objects.all(),
		}

		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		context = {}
		return render(request, self.template_name, context)

# Fetch the graph using id from plot.py 
class getGraphic(TemplateView):

	def get(self, request, *args, **kwargs):
		# taking graph id dynamically from input element
		function_idx = request.GET.get('graphicRequestDynamic')
		all_functions = inspect.getmembers(plot, inspect.isfunction)
		data = {}
		function_param = request.GET.get('function_param')
		print(function_param)
		if request.GET.get('graph_index'):
			function_idx = int(request.GET.get('graph_index'))
			print('getting graph: '+request.GET.get('graph_index'))

		else:
			print("FAILED: No value 'graph_index'")
			print("Possible functions:")
			for idx, func in enumerate(all_functions):
				print("{}  :  {}".format(idx, func))

		graph_func = all_functions[function_idx][1]

		if function_param:
			data['graph_ex'] = graph_func(function_param)
		else:
			data['graph_ex'] = graph_func()

		return HttpResponse(json.dumps(data), content_type="application/json")

	def post(self, request, *args, **kwargs):
		# change render to helper graphs
		graphicRequested = request.POST.get('graphicButton.val()')
		html = render_to_string('frontend/scroll.html', {'dishes': dishes})
		return HttpResponse(html)

# Calculate and display graph of leading drugs for the entered cell line name
class getCellLine(TemplateView):
	def get(self, request, *args, **kwargs):
		Combos = request.GET.get('cellLineRequestDynamic')
		print(Combos)
		entered_score=request.GET.get('score')
		print("score is:",entered_score)
		data={}
		if request.GET.get('c_name'):
			Combos = models.Combo.objects.all().exclude(name__contains="EDGE")
			print("inside cellLine")
			query=request.GET.get('c_name')
			Combos = Combos.filter(CellLine__cell_line__icontains = query)# HSA_score, Loewe_score, Bliss_score, ZIP_score, Chou_score
			print("entered cell line found:",query)
			print("Combos:",Combos)
			drugs_used = set() # set
			for combo in Combos:
				drugs_used.add(combo.drug_1)
				drugs_used.add(combo.drug_2)
				print("drugs used:",drugs_used)

			avg_score = {}
			print("avg:",avg_score)
			drugs=" "
			
			for drugs in drugs_used:
				
				avg_score[drugs] = list()
				
				for combo in Combos:
					if combo.drug_1 == drugs or combo.drug_2 == drugs:
						if entered_score == "Bliss_score":
							avg_score[drugs].append(combo.Bliss_score)
						elif entered_score == "Chou_score":
							avg_score[drugs].append(combo.Chou_score)
						elif entered_score == "ZIP_score":
							avg_score[drugs].append(combo.ZIP_score)
						else:
							avg_score[drugs].append(combo.HSA_score)

			print("all items:", avg_score.items())
			
			keys_values = avg_score.items()

			new_avg = {str(key):values for key,values in keys_values}

			print(new_avg)


			for key, values in new_avg.items():
				print(new_avg[key],values)
				new_avg[key] = sum(values)/len(values)
				print("avg_score:",new_avg)

			data['cell_response'] = plot.histogram(new_avg,"cellline: "+ query + " " + entered_score)
			
			print("plotted")
		return HttpResponse(json.dumps(data), content_type="application/json")

# Calculate and display graph of leading cell lines for the entered drug name
class getDrug(TemplateView):
	def get(self, request, *args, **kwargs):
		Combos = request.GET.get('drugRequestDynamic')
		print(Combos)
		entered_score=request.GET.get('score')
		print("score is:",entered_score)

		data={}
		if request.GET.get('d_name'):
			Combos = models.Combo.objects.all().exclude(name__contains="EDGE")
			query =	request.GET.get('d_name')
			Combos = Combos.filter( Q(drug_1__drug_name__icontains=query) | Q(drug_2__drug_name__icontains=query) )
			cell_Lines = set()
			[cell_Lines.add(combo.CellLine) for combo in Combos]    	
			avg_score = {}
			
			
			for CL in cell_Lines:
				avg_score[CL] = list()
				for combo in Combos:
					if combo.CellLine == CL:
						if entered_score == "Bliss_score":
							avg_score[CL].append(combo.Bliss_score)
						elif entered_score == "Chou_score":
							avg_score[CL].append(combo.Chou_score)
						elif entered_score == "ZIP_score":
							avg_score[CL].append(combo.ZIP_score)
						else:
							avg_score[CL].append(combo.HSA_score)

			print("all items:", avg_score.items())
			
			keys_values = avg_score.items()

			new_avg = {str(key):values for key,values in keys_values}

			print(new_avg)
	
			for key, values in new_avg.items():
				new_avg[key] = sum(values)/len(values)

			data['drug_response'] = plot.histogram(new_avg,"drug name: " + query + " " + entered_score)

		return HttpResponse(json.dumps(data), content_type="application/json")

# Calculate and display graph of leading drugs for the entered cancer name
class getIndication(TemplateView):
	def get(self, request, *args, **kwargs):
		query = request.GET.get('indicationRequestDynamic')
		print("inside get indication",query)
		entered_score=request.GET.get('score')
		print("score is:",entered_score)
		data={}
		if request.GET.get('i_name'):
			print("inside if")
			Combos = models.Combo.objects.all().exclude(name__contains="EDGE")
			query =	(request.GET.get('i_name'))
			print("found query is:",query)

			

			cancers=models.Cancer.objects.filter(cancer_type=query).values('id')
			print(cancers)
			Combos=Combos.filter(CellLine__indication__in=cancers)

			print("Combos:",Combos)
			drugs_used = set() # set
			for combo in Combos:
				drugs_used.add(combo.drug_1)
				drugs_used.add(combo.drug_2)	
				print("drugs used:",drugs_used)

			avg_score = {}
			print("avg:",avg_score)
			drugs=" "
			
			for drugs in drugs_used:
				
				avg_score[drugs] = list()
				
				for combo in Combos:
					if combo.drug_1 == drugs or combo.drug_2 == drugs:
						if entered_score == "Bliss_score":
							avg_score[drugs].append(combo.Bliss_score)
						elif entered_score == "Chou_score":
							avg_score[drugs].append(combo.Chou_score)
						elif entered_score == "ZIP_score":
							avg_score[drugs].append(combo.ZIP_score)
						else:
							avg_score[drugs].append(combo.HSA_score)	

			print("all items:", avg_score.items())
			
			keys_values = avg_score.items()

			new_avg = {str(key):values for key,values in keys_values}

			print(new_avg)


			for key, values in new_avg.items():
				new_avg[key] = sum(values)/len(values)

			data['indi_response'] = plot.histogram(new_avg,"cancer type: "+ query + " " + entered_score)
			
			print("plotted")
		return HttpResponse(json.dumps(data), content_type="application/json")

# Calculate and display graph of leading indications for the entered drug name
class getDrugforIndication(TemplateView):
	def get(self, request, *args, **kwargs):
		query = request.GET.get('drugIndicationRequestDynamic')
		print("inside get indication",query)
		entered_score=request.GET.get('score')
		print("score is:",entered_score)
		data={}
		if request.GET.get('drug_name'):

			print("inside if")
			Combos = models.Combo.objects.all().exclude(name__contains="EDGE")
			query =	(request.GET.get('drug_name'))
			print("found query is:",query)

			
			Combos = Combos.filter( Q(drug_1__drug_name__icontains=query) | Q(drug_2__drug_name__icontains=query) )
			print("drug filter:",Combos)

			Cancer = set()
			[Cancer.add(c.CellLine.indication.cancer_name) for c in Combos]  
			print("cancer names:", Cancer)
			avg_score = {}
			for CL in Cancer:
				avg_score[CL] = list()
				for combo in Combos:
					if combo.CellLine.indication.cancer_name == CL:
						if entered_score == "Bliss_score":
							avg_score[CL].append(combo.Bliss_score)
						elif entered_score == "Chou_score":
							avg_score[CL].append(combo.Chou_score)
						elif entered_score == "ZIP_score":
							avg_score[CL].append(combo.ZIP_score)
						else:
							avg_score[CL].append(combo.HSA_score)
			
			
			print("all items:", avg_score.items())
			
			keys_values = avg_score.items()

			new_avg = {str(key):values for key,values in keys_values}

			print(new_avg)


			for key, values in new_avg.items():
				new_avg[key] = sum(values)/len(values)

			data['drugIndi_response'] = plot.histogram(new_avg,"Drug name: "+ query + " " + entered_score)
			
			print("plotted")
		return HttpResponse(json.dumps(data), content_type="application/json")

# Calculate and display graph of best performing drugs for the entered drug 1 name
class getDrugvsDrug(TemplateView):
	def get(self, request, *args, **kwargs):
		Combos = request.GET.get('d1RequestDynamic')
		print(Combos)
		entered_score=request.GET.get('score')
		print("score is:",entered_score)

		data={}
		if request.GET.get('d1_name'):
			Combos = models.Combo.objects.all().exclude(name__contains="EDGE")
			query =	request.GET.get('d1_name')
			Combos = Combos.filter( Q(drug_1__drug_name__icontains=query))
			drug2 = set()
			[drug2.add(combo.drug_2) for combo in Combos]    	
			avg_score = {}
			
			
			for dr in drug2:
				avg_score[dr] = list()
				for combo in Combos:
					if combo.drug_2 == dr:
						if entered_score == "Bliss_score":
							avg_score[dr].append(combo.Bliss_score)
						elif entered_score == "Chou_score":
							avg_score[dr].append(combo.Chou_score)
						elif entered_score == "ZIP_score":
							avg_score[dr].append(combo.ZIP_score)
						else:
							avg_score[dr].append(combo.HSA_score)

			print("all items:", avg_score.items())
			
			keys_values = avg_score.items()

			new_avg = {str(key):values for key,values in keys_values}

			print(new_avg)
	
			for key, values in new_avg.items():
				new_avg[key] = sum(values)/len(values) if len(values) != 0 else 0

			data['dvd_response'] = plot.histogram(new_avg,"drug name: " + query + " " + entered_score)

		return HttpResponse(json.dumps(data), content_type="application/json")				

class getIc50(TemplateView):
	
	def get(self, request, *args, **kwargs):

		search = request.GET.get('search')
		print("search_text found is:", search)
		ic50s = models.Ic50.objects.filter(drug1_id__drug_name=search)		
		html = render_to_string('delve/ic50_results.html', {'ic50s': ic50s})
		return HttpResponse(html)
		
class possibleGraphics(TemplateView):
	# slug_url_kwarg = 'the_slug'

	def get(self, request, *args, **kwargs):
		all_functions = inspect.getmembers(plot, inspect.isfunction)
		print("Possible functions:")
		for idx, func in enumerate(all_functions):
			print("{}  :  {}".format(idx, func))


		return HttpResponse(json.dumps({}), content_type="application/json")

# Bubbles (Zoomable circle pack)
class cancer_json(TemplateView):
	def get(self, request, *args, **kwargs):
		# Example bubbles
		context = {"name": "Cancers", "children":[
											{"name":"Cancer Name","children":[
												{"name": "Cancer Name", "size":20},
											]},
											{"name":"Cancer Name1","children":[
												{"name": "Cancer Name", "size":12},
												{"name": "Cancer Name","size":17},
											]},
											{"name":"Cancer Name","children":[
												{"name": "Cancer Name", "children":[
													{"name": "Cancer Name", "size":17},
													{"name": "Cancer Name", "size":17},
												]},
												{"name": "Cancer Name", "size":17},
											]},
											{"name":"Cancer Name","size":17},
										],
					}

		##########################
		# Formatted Cancer table # 
		##########################

		# X-Y coordinates using x as gen and y as (class ID - ID). Embed in field in cancer model 
		# Iterate through and match by name


		# Add fields to combos, drugs, ic50's for cumputations on each page (its wasteful to do them again and again)
		# Make igrations for this AND for the x-y coordinates for each cancer model
		
		for idx, cancer in enumerate(models.Cancer.objects.all()):
			print('Index: %d \n Cancer: %s \n'%(idx, cancer.cancer_name))		
			if cancer.gen == 1:
				cancer_type_lst = context["children"]
				cancer_type_lst.append({'name':cancer.cancer_name})
				if not cancer.children_bool: 
					context["size"] = 15


		# 	elif cancer.gen == 2:
		# 		context["children"][idx]['name'] = cancer.cancer_name

		# 		if cancer.children_bool: # If child
		# 			context["children"][idx]['children'] = []
		# 		else:
		# 			context["children"][idx]['size'] = 10

		# 	elif cancer.gen == 3:
		# 		context["children"][idx]['children'][idx]['names'] = cancer.cancer_name
		# 		if cancer.children_bool: 
		# 			context["children"][idx]["children"][idx]["children"] = []
		# 		else:
		# 			context["children"][idx]["children"][idx]["size"] = 7

		# 	else:
		# 		context["children"][idx]['children'][idx]["children"][idx]['names'] = cancer.cancer_name
		# 		if cancer.children_bool:
		# 			context["children"][idx]["children"][idx]["children"][idx]["children"] = []
		# 		else:
		# 			context["children"][idx]["children"][idx]["children"][idx]["size"] = 5
		# return
		return JsonResponse(context)

class runMLServer(TemplateView): # done here to maintain CORS settigns (although could allow this server in settings.py, will research further at a later date)
	def post(self, request, *args, **kwargs):	
		ticket_data = dict(request.POST.items())
		ticket_files = dict(request.FILES.items())
		files = {}
		for memfile_key in ticket_files:
			io_file = request.FILES[memfile_key].file.getvalue()
			files.update({memfile_key: io_file})
		files.update({'data':json.dumps(ticket_data)})
		try:
			x = requests.post(
								'http://127.0.0.1:5000/run-model-284576d7777c8bcc7f1d74da39646787', 
								files 	= files, 
							)	
			# return JsonResponse(json.loads(x.content), safe=False)
			try:
				return JsonResponse(json.loads(x.content))
			except Exception as e:
				print('content unexpected:',str(e))
				return JsonResponse({'response error':'content unexpected', 'exception':str(e)})
		
		except Exception as e:
			print('no response from server:',str(e))
			return JsonResponse({'request error':'no response from server', 'exception':str(e)})

# -------- FOR DEBUGGING ONLY!!!!!!! ------------------------------------
from django.views.decorators.csrf import csrf_exempt   	# ---------------
from django.utils.decorators import method_decorator	# ---------------
@method_decorator(csrf_exempt, name='dispatch')
class runMLServer_V2(TemplateView): # done here to maintain CORS settigns (although could allow this server in settings.py, will research further at a later date)
	def post(self, request, *args, **kwargs):	
		# Upload all data to S3
		# Get specific folder tag for request
		# Send folder to Flask
		# Flask app uses data + s3_uri sent from post request to determine which ml function
		# uses uri to get all data from specific s3 folder and run
		# uploads back to same folder: output-success.csv OR output-failure.csv
		ticket_data = dict(request.POST.items())
		ticket_files = dict(request.FILES.items())
		files = {}
		print(ticket_data.keys())
		print(ticket_files.keys())
		for memfile_key in ticket_files:
			file = request.FILES[memfile_key].file
			AWS_helper.upload_df_or_file_to_s3(file, path = 'run-request-data-in/')
		# ::::::::::   READ TEUSDAY MORNING FOR CONITNUING WHAT TO DO   :::::::::: 
		# TODO add upload in parts for extremely large file uploads
		# TODO have it create unqiue folders for each run ticket to hold in and out data --> then to db
		# TODO have flask pull from needed folder via uri passed in request and put in output data from run
		# Figure out automating large number of jobs and uploads 
		return JsonResponse({'RunMLv2':'view has run', 'stage':'testing s3 uploads'})

class saveMLRunResults(TemplateView): # done here to maintain CORS settigns (although could allow this server in settings.py, will research further at a later date)
	def post(self, request, *args, **kwargs):
		given = list(request.POST.items())
		rs = dict(given)
		if 'error' in rs or 'Error' in rs:
			for key in rs:
				print('key: {} \nval: {}'.format(key, rs[key]))
			return JsonResponse(rs)
		elif 'URIs' not in rs or 'tags' not in rs:
			return JsonResponse({'response error':'content unexpected', 'reason':'missing keys'})

		rs['URIs'] = rs['URIs'].split(',')
		rs['tags'] = rs['tags'].split(',')
		new_ML_report = models.ML_Result(ml_type = rs['selected_model'], by_user = request.user.__str__())
		new_ML_report.save()
		for new_tag in rs['tags']:
			new_tag_inst = models.Tag(name = new_tag)
			try:
				new_tag_inst.save()
			except:
				print(new_tag)
				new_tag_inst = models.Tag.objects.get(name = new_tag)
			new_ML_report.tags.add(new_tag_inst)
			new_ML_report.save()

		for new_file in rs['URIs']:
			new_file_save = models.S3_File(name = str(rs['selected_model']+new_file), uri = new_file, ML_Result_fk = new_ML_report)
			try:
				new_file_save.save()
			except:
				continue
		print(list(rs['data']))
		# for report_tuple in rs['run_Tags_and_URIs'].split(','):
		# 	print((report_tuple))
		# 	print(tuple(report_tuple))
		# 	tag_lst = tuple(report_tuple)[0]
		# 	uri_lst = tuple(report_tuple)[1]
		# 	print('tag_lst:{}\nuri_lst:{}\n'.format(tag_lst,uri_lst))
		# 	pass
		return JsonResponse({"success":"saved"})

class getMLReport(TemplateView):
	def get(self, request, *args, **kwargs):
		report_matrix = []
		all_reports = models.ML_Result.objects.all()
		for report in all_reports:
			files_html = '<div class="row">'
			for idx, file_inst in enumerate(report.s3_file_set.all()):
				uri_div = '<a href="'+file_inst.uri+'" class="btn btn-primary mr-2" target="_blank">File '+str(idx)+'</a>'
				files_html+=(uri_div) 
			files_html+=('</div>')
			report_matrix.append([
				str(report.date_run),
				report.ml_type,
				report.by_user,
				files_html,
				list(report.tags.all().values_list('name', flat=True).order_by('id')),
				'<button id="ml-report-"'+str(report.id)+' class="btn btn-info">Report</button>'
			])
		return HttpResponse(json.dumps(report_matrix), content_type="application/json")



