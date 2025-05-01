from django.shortcuts import render
from django.http import HttpResponse
from myapp.models import Application

def home(request):
    return render(request, 'hello.html')

def submit(request):
    if request.method == 'POST':
        # Access form data from the POST request
        positionTitle = request.POST.get('positionTitle')
        companyName = request.POST.get('companyName')
        jobCategory = request.POST.get('jobCategory')
        coverLetter = request.POST.get('coverLetter')
        discoveryMethod = request.POST.get('discoveryMethod')

        if (positionTitle is "" or companyName is "" or jobCategory is ""
            or coverLetter is "" or discoveryMethod is ""):
            return render(request, 'error.html')

        # Insert Data into PostgreSQL
        a = Application(positionTitle=positionTitle, companyName=companyName,
                        jobCategory=jobCategory, coverLetter=coverLetter, discoveryMethod=discoveryMethod)
        a.save()
        
        # Now you can use this data, for example, validate or store it
        return render(request, 'success.html')
    else:
        return render(request, 'hello.html')
