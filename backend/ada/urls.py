from django.urls import path
from ada import views
from ada import plots
from wkhtmltopdf.views import PDFTemplateView

urlpatterns = [
    path('upload',views.upload.as_view(),name='upload'),
    path('report/<id>', views.report_page.as_view(),name='Report'),
    path('processed', views.report_page.as_view(),name='Process'),
    path('pdf', views.report_page.as_view(), name='GET_PDF'),
    # path(r'^pdf/$', PDFTemplateView.as_view(template_name='my_template.html', filename='my_pdf.pdf'), name='GET_PDF'),
    # path(r'^pdf/$', PDFTemplateView.as_view(template_name='delve/CI_report.html', filename='my_pdf.pdf'), name='GET_PDF'),
]


