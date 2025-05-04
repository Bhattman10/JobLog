from django.shortcuts import render
from django.http import HttpResponse
from myapp.models import Application
from django.db.models import Q

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
            return render(request, 'error.html', {'error': "One or more fields are missing."})

        # Insert Data into PostgreSQL
        a = Application(positionTitle=positionTitle, companyName=companyName,
                        jobCategory=jobCategory, coverLetter=coverLetter, discoveryMethod=discoveryMethod)
        a.save()
        
        return render(request, 'success.html')
    
    else:
        return render(request, 'hello.html')

def view(request):
    # Retrieve tuples and format into string.
    display_of_applications = ""
    for a in Application.objects.all():
        str_tuple = "[" + str(a.id) + "] " + str(a.date) + " | " + a.positionTitle + " | " + a.companyName + " | " + a.jobCategory + " | " + a.coverLetter + " | " + a.discoveryMethod + " | " + str(a.interviewCount) + " | " + str(a.jobOffer)
        display_of_applications += str_tuple
        display_of_applications += "\n"
    return render(request, 'view.html', {'display_of_applications': display_of_applications})

def update(request):
    if request.method == 'POST':
        # Collect data from form submission
        application_id = request.POST.get('application_id')
        field_to_update = request.POST.get('field_to_update')
        new_field_value = request.POST.get('new_value')

        # Check if any fields are empty
        if(application_id == "" or field_to_update == "" or new_field_value == ""):
            return render(request, 'error.html', {'error' : "One or more fields are missing."})
        
        # Check if ID entered is an integer
        try:
            application_id = int(application_id)
        except (TypeError, ValueError):
            return render(request, 'error.html', {'error' : "The value entered is not an integer."})
        
        # Check if ID entered exists in database
        if(not Application.objects.filter(id=application_id).exists()):
            return render(request, 'error.html', {'error' : "The ID entered does not exist."})
        
        # Check if the new value entered matches the required data type prior to updating the value.
        a = Application.objects.get(id=application_id)
        if(field_to_update == "positionTitle"):
            a.positionTitle = new_field_value
        elif(field_to_update == "companyName"):
            a.companyName = new_field_value
        elif(field_to_update == "jobCategory"):
            if(new_field_value != "software_developer" or new_field_value != "data_analytics"
               or new_field_value != "information_technology" or new_field_value != "business_and_sales"):
                return render(request, 'error.html', {'error' : "!= [software_developer] [data_analytics] [information_technology] [business_and_sales]"})
            a.jobCategory = new_field_value
        elif(field_to_update == "coverLetter"):
            if(new_field_value != "no" or new_field_value != "yes"):
                return render(request, 'error.html', {'error' : "!= [yes] [no]"})
            a.coverLetter = new_field_value
        elif(field_to_update == "discoveryMethod"):
            if(new_field_value != "indeed" or new_field_value != "linkedin" or new_field_value != "reference"):
                return render(request, 'error.html', {'error' : "!= [indeed] [linkedin] [reference]"})
            a.discoveryMethod = new_field_value
        elif(field_to_update == "interviewCount"):
            try:
                new_field_value = int(new_field_value)
            except (TypeError, ValueError):
                return render(request, 'error.html', {'error' : "The value entered is not an integer."})
            a.interviewCount = new_field_value
        elif(field_to_update == "jobOffer"):
            if(new_field_value != "t" or new_field_value != "f"):
                return render(request, 'error.html', {'error' : "!= [t] [f]"})
            a.jobOffer = new_field_value
        a.save()
            

        return render(request, 'success.html')
    else:
        return render(request, 'update.html')

def stats(request): #TODO
    if request.method == 'POST':
        filter_software_developer = request.POST.get('software_developer')
        filter_data_analytics = request.POST.get('data_analytics')
        filter_information_technology = request.POST.get('information_technology')
        filter_business_and_sales = request.POST.get('business_and_sales')
        filtered_applications = Application.objects.filter(Q(jobCategory=filter_software_developer)
                                                           | Q(jobCategory=filter_data_analytics)
                                                           | Q(jobCategory=filter_information_technology)
                                                           | Q(jobCategory=filter_business_and_sales))
        filtered_applications_with_interviews = Application.objects.filter((Q(jobCategory=filter_software_developer)
                                                                           | Q(jobCategory=filter_data_analytics)
                                                                           | Q(jobCategory=filter_information_technology)
                                                                           | Q(jobCategory=filter_business_and_sales))
                                                                           & ~Q(interviewCount=0))
        stat_display = "Percentage of applications with at least one interview = %"
        if filtered_applications.exists():
            percent = filtered_applications_with_interviews.count() / filtered_applications.count()
            truncated_percent = round(percent, 2)
            stat_display += str(truncated_percent)
        else:
            stat_display += "0.00"
            

        return render(request, 'stats.html', {'stat_display': stat_display})
    else:
        return render(request, 'stats.html')