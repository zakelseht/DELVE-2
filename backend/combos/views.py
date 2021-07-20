# class based views

from django.shortcuts import render
from django.views.generic.edit import FormMixin
from django.views.generic import DetailView, ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q

from delve import models
from helper import plot, tox_plot
import json
def index(request):
		return render(request, 'combos/combos.html', {})

def graph_d3(request):
		return render(request, 'combos/plot_d3_test.html', {})

class combos_class(LoginRequiredMixin, TemplateView, FormMixin):
	login_url = '/user_login/'
	redirect_field_name = 'user_login'
	template_name = 'combos/combo_REST.html'

	def get(self, request, *args, **kwargs):
		Combos = models.Combo.objects.all().exclude(name__contains="EDGE")
		page = request.GET.get('page')

		# Handle get requests 
		if request.GET.get('report-filter'): # Filter by 1 of 5 scores: 
			# filter value contains either: HSA_score, Loewe_score, Bliss_score, ZIP_score, Chou_score
			print(request.GET.get('report-filter'))
			Combos = Combos.order_by(request.GET.get('report-filter'))[::-1]

		elif request.GET.get('cell-line'):
			query =	request.GET.get('cell-line')
			Combos = Combos.filter(CellLine__cell_line__icontains = query)
			
		elif request.GET.get('drug'):
			query =	request.GET.get('drug')
			Combos = Combos.filter( Q(drug_1__drug_name__icontains=query))

		content = {
			'combos': Paginator(Combos, 7).get_page(page)
		}
		return render(request, self.template_name, content)

	def post(self, request, *args, **kwargs):
		res = models.Combo.objects.all()
		return render(request, self.template_name, {'ic50': res})


	def get_context_data(self, **kwargs):
		"""
		get_context_data is one of the important hooks in generic class
		based views. It lets you add extra variables to the template context
		"""
		# Call the base implementation first to get a context
		context = super().get_context_data(**kwargs)
		# Add in a QuerySet of all the books
		context['book_list'] = models.Combo.objects.all()
		return context














































# from rest_framework import viewsets
# from combos import serializers
# class UserViewSet(viewsets.ModelViewSet):
# 	"""
# 	API endpoint that allows users to be viewed or edited.
# 	"""
# 	# queryset = models.User.objects.all().order_by('-date_joined')
# 	queryset = models.Profile.objects.all().order_by('-date_joined')
# 	serializer_class = serializers.UserSerializer


# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = models.Group.objects.all()
#     serializer_class = serializers.GroupSerializer



# from two_factor.views.mixins import OTPRequiredMixin
# from django.contrib.auth import authenticate, login, logout
# from django.http import HttpResponseRedirect, HttpResponse
# from django.views.generic import FormView
# from django.contrib.auth.decorators import login_required
# from django.urls import reverse

# from datetime import date
# from haystack.generic_views import SearchView
# from rest_framework import viewsets
# from combos import serializers
# from keras.models import load_model
# from delve_site.settings import MODEL_CMD
		# NN_model = load_model(MODEL_CMD)
		# NN_model.summary()
		# NN_model.predict()
