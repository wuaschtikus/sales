from django.views.generic import ListView, DetailView, FormView
from .forms import MyFileUploadForm
from django.shortcuts import render
from django.views import View


class IndexView(View):
    template_name = 'msgconv/index.html'
    def get(self, request):
        return render(request, self.template_name)
    
class ConverterView(View):
    template_name = 'msgconv/converter.html'
    def get(self, request):
        return render(request, self.template_name)

class MsgConv(View):
    template_name = 'msgconv/msgconv.html'
    
    def get(self, request):
        form = MyFileUploadForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = MyFileUploadForm(request.POST, request.FILES)
        print(request.__dict__)
        if form.is_valid():
            # Process the file here
            uploaded_file = request.FILES['file']
            file_content = uploaded_file.read()  # This reads the file into memory
            # You can then process the file_content as needed
            print(file_content)
            return render(request, self.template_name, {'file_name': uploaded_file.name})
        return render(request, self.template_name, {'form': form})
