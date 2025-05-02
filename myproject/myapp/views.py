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

        # Check if user forgot to enter a field and return error message.
        if (positionTitle == "" or companyName == "" or jobCategory == "" or coverLetter == "" or discoveryMethod == ""):
            return render(request, 'error.html')

        # Insert Data into PostgreSQL
        a = Application(positionTitle=positionTitle, companyName=companyName,
                        jobCategory=jobCategory, coverLetter=coverLetter, discoveryMethod=discoveryMethod)
        a.save()
        
        return render(request, 'success.html')
    
    else:
        return render(request, 'hello.html')

def view(request): #TODO
    # Retrieve tuples and format into string.
    display_of_applications = ""
    for a in Application.objects.all():
        str_tuple = "[" + str(a.id) + "] " + str(a.date) + " | " + a.positionTitle + " | " + a.companyName + " | " + a.jobCategory + " | " + a.coverLetter + " | " + a.discoveryMethod + " | " + str(a.interviewCount) + " | " + str(a.jobOffer)
        display_of_applications += str_tuple
        display_of_applications += "\n"
    return render(request, 'view.html', {'display_of_applications': display_of_applications})

def update(request): #TODO
    return render(request, 'update.html')

def stats(request): #TODO
    return render(request, 'stats.html')