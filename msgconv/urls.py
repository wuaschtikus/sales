from django.urls import path
from .views import MsgConv, IndexView, ConverterView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('converter/', ConverterView.as_view(), name='converter'),
    path('msgconv/', MsgConv.as_view(), name='msgconv'),
    path('upload/', MsgConv.as_view(), name='msgupload'),
]