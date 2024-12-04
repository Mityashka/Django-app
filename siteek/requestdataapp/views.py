from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest
from django.shortcuts import render
from .forms import USerBioForm, UploadFilesForm

def process_get_view(request: HttpRequest):
    a = request.GET.get('a', '')
    b = request.GET.get('b', '')
    result = a + b
    context = {
        'a': a,
        'b':b,
        'result':result,
    }
    return render(request, 'requestdataapp/request-query-params.html', context = context)

def user_form(request: HttpRequest):
    form = USerBioForm()
    context = {
        "form":form,
    }
    return render(request, 'requestdataapp/user-bio-form.html', context=context)

def handle_file_upload(request: HttpRequest):
    if request.method == 'POST':
        form = UploadFilesForm(request.POST, request.FILES)
        if form.is_valid():
            myfile = form.cleaned_data['file']
            Fs = FileSystemStorage()
            filename = Fs.save(myfile.name, myfile)
            print(f'Save file {filename}')
    else:
        form = UploadFilesForm()
    context = {
        'form':form,
    }
    return render(request, 'requestdataapp/file-upload.html', context=context)