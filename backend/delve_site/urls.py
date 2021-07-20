# from delve import views
from delve import views, ajax
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static


admin.autodiscover()
urlpatterns = [
	
	path('',									views.DashView.as_view()),
	path('admin/', 								admin.site.urls, name='admin'),

	path('user_login/',							views.user_login,name='user_login'),
	path('logout/', 							views.user_logout, name='logout'),

	# Nav Pages 
	path('dash/',								views.DashView.as_view(),name='dash'),
	path('dash/',								views.DashView.as_view(),name='index'),
	path('M2M/',								views.M2M_View.as_view(), name='ML_GV'),
	path('report_idx/',							views.report_idx.as_view(),name='report_index'),
	path('404', 								views.page_404, name='404'),
		
	# Wireframes
	# path('slack/', 											views.slack_shorcut_view.as_view(),name='slack'),
	path('Drugs/', 											views.drug_view.as_view(),name='Drugs'),
	path('Automation/', 									views.automation_page_select_view.as_view(),name='Automation'),
	path('Automation/TicketTable', 							views.automation_page_ticket_table_view.as_view(),name='Automation'),
	path('IC50/<int:combo_id>-<int:drug_id>', 				views.ic50_discrete_view.as_view(),name='ic50_discrete'),
	path('Cancers/', 										views.cancer_page_view.as_view(),name='cancers'),
	path('Cancers/', 										views.cancer_page_view.as_view(),name='cancer-search'),
	path('Cancers/overview', 								views.cancer_overview_view.as_view(),name='cancer-overview'),
	path('Cancers/detail/<int:cancer_id>', 					views.cancer_detail_redirect.as_view(),name='cancer-detail-redirect'),
	path('Cancers/detail/<str:name>-<int:cancer_id>', 		views.cancer_detail_view.as_view(),name='cancer-detail'),

	# ================================================================================================ 

	# Other Apps
	path('',				include('ada.urls')),
	path('combos/',			include('combos.urls')),

	# Admin Specific
	path('quick/data/', 						views.quickData.as_view(), name='quickData'), 
	path('docs', 								(views.docs.as_view()), name='documentation'), 
	path('83d59063f74c9556d4595117d53dee45', 	views.is_authenticated, name="check-if-user"),
	
	# Depricated Data Requests
	path('cancer-autocomplete/', 	views.CellLineAutoComplete.as_view(), name='cancer-autocomplete'),		
	path('ic50-autocomplete/', 		views.DrugAndCellLineAutoComplete.as_view(), name='ic50-autocomplete'),
	path('cell-autocomplete/',		views.CellAutoComplete.as_view(),name='cell-autocomplete'),	
	path('nav-autocomplete/', 		views.NavAutoComplete.as_view(), name='nav-autocomplete'),	



	# Ajax
	# ================================================================================================ 
	path('API/SMILESRequest/', 			ajax.SMILESRequest.as_view(), name='SMILESRequest'),	
	path('API/cellLineRequest/', 		ajax.getCellLine.as_view(), name='cellLineRequest'),
	path('API/drugRequest/', 			ajax.getDrug.as_view(), name='drugRequest'),	
	path('API/indicationRequest/', 		ajax.getIndication.as_view(), name='indicationRequest'),	
	path('API/drugIndicationRequest/', 	ajax.getDrugforIndication.as_view(), name='drugIndicationRequest'),	
	path('API/drugvsdrugRequest/', 		ajax.getDrugvsDrug.as_view(), name='drugvsdrugRequest'),	
	path('API/nav/', 					ajax.NavAutoComplete.as_view(), name='api-nav'),	
	path('API/nav/', 					views.NavAutoComplete.as_view(), name='api-nav'),	
	path('API/nav/options', 			ajax.GlobalNavSearchOptions.as_view(), name='api-nav-options'),	
	path('API/nav/options',			 	ajax.GlobalNavSearchOptions.as_view(), name='api-nav-options'),	
	path('API/graphicRequest/', 		ajax.getGraphic.as_view(), name='graphicRequest'),	
	path("API/ic50search/", 			ajax.getIc50.as_view(), name='ic50search'),
	path("API/MLRequest/", 				ajax.runMLServer.as_view(), name='MLReq'), 		#  / V1. \
	path("API/MLRequestV2/", 			ajax.runMLServer_V2.as_view(), name='MLReq'), 	#  \ V2. /
	path("API/MLSave/", 				ajax.saveMLRunResults.as_view(), name='MLSave'),
	path("API/getMLReport/", 			ajax.getMLReport.as_view(), name='MLRepoLst'),
		
	# path("API/ic50search/", 			views.ic50Search_view.as_view(), name="ic50search"),

	# path('ajax/nav/', ajax.NavAutoComplete.as_view(), name='api-nav'),	
	# path('ajax/graphicRequest/<slug:slug>', ajax.NavAutoComplete.as_view(), name='graphicRequest'),	
	# ================================================================================================ 


	# path('Cancers/flare.json', 				views.cancer_json.as_view()),
	
	path('IC50Search/', 						views.Ic50Search.as_view(),name='ic50_search'),
	path('cellLine/',							views.cellLine_view.as_view(),name='cellLine_search'),
	# Wireframes
	# path('IC50/', 								views.ic50_view.as_view(),name='ic50'),
	path('Cancers/', 							views.cancer_page_view.as_view(),name='cancers'),
	# path('Cancers/flare.json', 					views.cancer_json.as_view()),
	path('combos/',								include('combos.urls')),
	# path('IC50Search/', 						views.ic50Search_view.as_view(),name='ic50_search'),

	# 2FA (Twilio/authy)
	# ================================================================================================ 
	path('register/', 				views.TwoFA_register, name='register'),
	path('2FA/2fa/', 				views.TwoFA_twofa, name='twilio_2fa'),
	path('2FA/token/sms', 			views.TwoFA_token_sms, name='twilio_token-sms'),
	path('2FA/token/voice', 		views.TwoFA_token_voice, name='twilio_token-voice'),
	path('2FA/token/onetouch', 		views.TwoFA_token_onetouch, name='twilio_token-onetouch'),  # noqa: E501
	path('2FA/protected/', 			views.TwoFA_protected, name='twilio_protected'),
	path('2FA/onetouch-status', 	views.TwoFA_onetouch_status, name='twilio_onetouch-status'),  # noqa: E501

	path('', 						views.TwoFA_home, name='twilio_home'),
	# # ================================================================================================ 

	# # May need to add or remove
	# path('IC50Search/',			views.ic50Search_view.as_view(),name='ic50_search'),
	path('quick/data/', 		views.quickData.as_view(), name='quickData'), 
	path('docs', 				views.docs.as_view(), name='documentation'), 

	# # path('ajax/nav/', ajax.NavAutoComplete.as_view(), name='api-nav'),	
	# # path('ajax/graphicRequest/<slug:slug>', ajax.NavAutoComplete.as_view(), name='graphicRequest'),	



	# # 2FA
	# path('', 					include(tf_urls)),

]
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
