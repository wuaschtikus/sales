from django.urls import path
from .views import MsgConv, IndexView, ConverterView, DeleteFiles

urlpatterns = [
    path('index/', IndexView.as_view(), name='index'),
    path('converter/', ConverterView.as_view(), name='converter'),
    path('msgconv/', MsgConv.as_view(), name='msgconv'),
    path('msgconv/<str:id>', MsgConv.as_view(), name='msgconv'),
    path('upload/', MsgConv.as_view(), name='msgupload'),
    path('delete/<str:id>', DeleteFiles.as_view(), name='delete_files'),
]