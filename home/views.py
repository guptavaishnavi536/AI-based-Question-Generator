import os
from django.conf import settings
from django.shortcuts import render, HttpResponse
from home.models import Queries, Login
from . import forms,models
from .forms import QueriesForm
from .forms import LoginForm
from .forms import SignupForm
from .forms import QnAForm
from . import gen

# Create your views here.
def index(request):
    context = {
        "variable1" : "Hie this is Generate.AI"
    }
    return render(request, 'index.html', context)
    # return HttpResponse("This is Home Page")

def home(request):
    return render(request, 'home.html')
    # return HttpResponse("This is Home Page")

# def about(request):
#     return render(request, 'about.html')
    # return HttpResponse("This is About Us Page")

def services(request):
    return render(request, 'services.html')
    # return HttpResponse("This is Services Page")

# def queries(request):
#     return render(request, 'queries.html')
#     # return HttpResponse("This is queries Page")
    

def queries(request):   
    if request.method == "POST":
        form=QueriesForm(request.POST)
        if form.is_valid():
          form.save()
    else:
        form=QueriesForm()                     
    return render(request, 'queries.html', {'form': form})
    # return HttpResponse("This is queries Page")




from home.forms import QnAForm  


# def QnA(request):
#     form = QnAForm()
#     if request.method=='POST':
#         form = QnAForm(request.POST, request.FILES)
#         pdf = request.POST.get('pdf')
#         request.session['pdf'] = pdf #saving the pdf path in the django session
     
#         gen.generate(pdf, 'qna', 'qna')

#         # to call this in another function use:
#         # pdf = request.session.get('pdf')
#         if form.is_valid():
#             user=form.save()
#             user.save()
#         return HttpResponse('Uploaded')
    

#     return render(request,'QnA.html')

def QnA(request):
    form = QnAForm()
    if request.method=='POST':
        form = QnAForm(request.POST, request.FILES)
        # pdf = request.POST.get('pdf')
        # request.session['pdf'] = pdf #saving the pdf path in the django session
 
 
        if form.is_valid():
            user=form.save()
            user.save()
            pdf_file = form.cleaned_data['pdf']
            file_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', pdf_file.name)
            # request.session['file_path'] = file_path #saving the pdf path in the django session
 
            # to call this in another function use:
            # file_path = request.session.get('file_path')
        # string = str(file_path).replace("\\\\", "\\")
                                

        gen.generate("media/pdf/"+pdf_file.name, 'qna')

        # return HttpResponse(file_path)

        # return HttpResponse('File Saved Successfully.')
        return render(request, 'saved.html')
    return render(request,'QnA.html')
    
def mcq(request):
    form = QnAForm()
    if request.method=='POST':
        form = QnAForm(request.POST, request.FILES)
        # pdf = request.POST.get('pdf')
        # request.session['pdf'] = pdf #saving the pdf path in the django session
 
 
        if form.is_valid():
            user=form.save()
            user.save()
            pdf_file = form.cleaned_data['pdf']
            file_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', pdf_file.name)
            # request.session['file_path'] = file_path #saving the pdf path in the django session
 
            # to call this in another function use:
            # file_path = request.session.get('file_path')
        # string = str(file_path).replace("\\\\", "\\")
                                

        gen.generate("media/pdf/"+pdf_file.name, 'mcq')

        # return HttpResponse('File Saved Successfully.')
        return render(request, 'saved.html')
    return render(request, 'mcq.html')
    # return HttpResponse("This is About Us Page")

def TnF(request):
    form = QnAForm()
    if request.method=='POST':
        form = QnAForm(request.POST, request.FILES)
        # pdf = request.POST.get('pdf')
        # request.session['pdf'] = pdf #saving the pdf path in the django session
 
 
        if form.is_valid():
            user=form.save()
            user.save()
            pdf_file = form.cleaned_data['pdf']
            file_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', pdf_file.name)
            # request.session['file_path'] = file_path #saving the pdf path in the django session
 
            # to call this in another function use:
            # file_path = request.session.get('file_path')
        # string = str(file_path).replace("\\\\", "\\")
                                

        gen.generate("media/pdf/"+pdf_file.name, 'tnf_v2')

        # return HttpResponse('File Saved Successfully.')
        return render(request, 'saved.html')
    return render(request, 'TnF.html')
    # return HttpResponse("This is Services Page")

def fill(request):
    form = QnAForm()
    if request.method=='POST':
        form = QnAForm(request.POST, request.FILES)
        # pdf = request.POST.get('pdf')
        # request.session['pdf'] = pdf #saving the pdf path in the django session
 
 
        if form.is_valid():
            user=form.save()
            user.save()
            pdf_file = form.cleaned_data['pdf']
            file_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', pdf_file.name)
            # request.session['file_path'] = file_path #saving the pdf path in the django session
 
            # to call this in another function use:
            # file_path = request.session.get('file_path')
        # string = str(file_path).replace("\\\\", "\\")
                                

        gen.generate("media/pdf/"+pdf_file.name, 'fib')

        # return HttpResponse('File Saved Successfully.')
        return render(request, 'saved.html')
    return render(request, 'fill.html')
    # return HttpResponse("This is queries Page")

def combine(request):
    form = QnAForm()
    if request.method=='POST':
        form = QnAForm(request.POST, request.FILES)
        # pdf = request.POST.get('pdf')
        # request.session['pdf'] = pdf #saving the pdf path in the django session
 
 
        if form.is_valid():
            user=form.save()
            user.save()
            pdf_file = form.cleaned_data['pdf']
            file_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', pdf_file.name)
            # request.session['file_path'] = file_path #saving the pdf path in the django session
 
            # to call this in another function use:
            # file_path = request.session.get('file_path')
        # string = str(file_path).replace("\\\\", "\\")
                                

        gen.generate("media/pdf/"+pdf_file.name, 'combined')

        # return HttpResponse('File Saved Successfully.')
        return render(request, 'saved.html')
    return render(request, 'combine.html')
    # return HttpResponse("This is queries Page")
    
def history(request):
    return render(request, 'history.html')
    # return HttpResponse("This is queries Page")

def login(request):
    if request.method == "POST":
        form=LoginForm(request.POST)
        if form.is_valid():
          form.save()
        else:
            form=LoginForm()
    return render(request, 'login.html')
    # return HttpResponse("This is queries Page")
    
def signup(request):
    if request.method == "POST":
        form= SignupForm(request.POST)
        if form.is_valid():
          form.save()
        else:
            form=SignupForm()
    return render(request, 'signup.html')
    # return HttpResponse("This is queries Page")
    

