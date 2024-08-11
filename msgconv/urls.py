from django.urls import path
from .views import IndexView, ConverterView, DeleteFiles, MsgConvMultipleFiles, MsgConvSingleFiles
from django.views.generic.base import TemplateView

urlpatterns = [
    path('index/', IndexView.as_view(), name='index'),
    path('converter/', ConverterView.as_view(), name='converter'),
    path('msgconv/single', MsgConvSingleFiles.as_view(), name='msgconv_single_files'),
    path('msgconv/single/<str:id>', MsgConvSingleFiles.as_view(), name='msgconv_single_files'),
    path('msgconv/multiple', MsgConvMultipleFiles.as_view(), name='msgconv_multiple_files'),
    path('msgconv/multiple/<str:id>', MsgConvMultipleFiles.as_view(), name='msgconv_multiple_files'),
    path('upload/', MsgConvSingleFiles.as_view(), name='msgupload'),
    path('delete/<str:id>', DeleteFiles.as_view(), name='delete_files'),
    path('about/', TemplateView.as_view(template_name='base/about.html'), name='about'),
    path('privacy/', TemplateView.as_view(template_name='base/privacy.html'), name='privacy'),
]