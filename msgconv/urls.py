from django.urls import path
from .views import IndexView, ConverterView, DeleteFiles, MsgConvMultipleFiles, MsgConvSingleFiles, ContactView, Subscription
from django.views.generic.base import TemplateView

urlpatterns = [
    path('index/', IndexView.as_view(), name='index'),
    path('converter/', ConverterView.as_view(), name='converter'),
    path('converter/single-files', MsgConvSingleFiles.as_view(), name='msgconv_single_files'),
    path('converter/single-files/<str:id>', MsgConvSingleFiles.as_view(), name='msgconv_single_files'),
    path('converter/multiple-files', MsgConvMultipleFiles.as_view(), name='msgconv_multiple_files'),
    path('converter/multiple-files/<str:id>', MsgConvMultipleFiles.as_view(), name='msgconv_multiple_files'),
    # path('msgconv/excel', MsgConvExcelFiles.as_view(), name='msgconv_excel_files'),
    # path('msgconv/excel/<str:id>', MsgConvExcelFiles.as_view(), name='msgconv_excel_files'),
    path('upload/', MsgConvSingleFiles.as_view(), name='msgupload'),
    path('converter/delete-files/<str:id>', DeleteFiles.as_view(), name='delete_files'),
    path('about/', TemplateView.as_view(template_name='base/about.html'), name='about'),
    path('privacy/', TemplateView.as_view(template_name='base/privacy.html'), name='privacy'),
    path('contact/', ContactView.as_view(template_name='base/contact.html'), name='contact'),
    path('faq/', TemplateView.as_view(template_name='base/faq.html'), name='faq'),
    path('subscription/', Subscription.as_view(), name='subscription'),
    path('starter/', TemplateView.as_view(template_name='base/enroll.html'), name='enroll-starter'),
    path('pro/', TemplateView.as_view(template_name='base/enroll.html'), name='enroll-pro'),
    path('premium/', TemplateView.as_view(template_name='base/enroll.html'), name='enroll-premium'),
]