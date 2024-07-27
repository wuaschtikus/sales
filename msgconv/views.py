from django.views.generic import ListView, DetailView, FormView
from .forms import MyFileUploadForm
from django.shortcuts import render
from django.views import View


class LandingView(View):
    template_name = 'index.html'
    def get(self, request):
        form = MyFileUploadForm()
        return render(request, 'index.html', {'form': form})

    def post(self, request):
        form = MyFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the file here
            title = form.cleaned_data['title']
            uploaded_file = request.FILES['file']
            file_content = uploaded_file.read()  # This reads the file into memory
            # You can then process the file_content as needed
            
            return render(request, 'index.html', {'title': title, 'file_name': uploaded_file.name})
        return render(request, 'index.html', {'form': form})
