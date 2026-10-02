
import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import EmployeeDetails
from django.views.decorators.csrf import csrf_exempt
import bcrypt
from.serializers import EmployeeDetailsSerializer
from.validations import password_check, password_hash
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives  
from django.template.loader import render_to_string  
from django.core.files.storage import FileSystemStorage
mail = settings.EMAIL_HOST_USER 
# Create your views here.
@csrf_exempt
def entry_page(req):
    valid = False
    if req.method =='POST':
       username = req.POST.get('username') 
       password = req.POST.get('password')
       print(username)
       print(password)
       emp_obj = EmployeeDetails.objects.get(username=username)
       print(emp_obj)
       if password == emp_obj.password:
           response =  JsonResponse({'status':'cookie set'})
           response.set_cookie(
               key = 'logged_in',
               value = True
               
           )
           return response         
       else:
            valid = True
            return render(req,'login.html',{'valid':valid})   
    return render(req,'login.html',{'valid':valid})

@csrf_exempt
def home(req):
    if 'username' in req.session:
        return JsonResponse({'status':'this is home page'})
    else:
        return JsonResponse({'status':'login first'})


# def dark_theme(req):
#     response =  JsonResponse({'status':'Theme set!'})
#     response.set_cookie(
#         key = 'Theme',
#         value = 'Dark'      
#     )
#     return response

def logout(req):
    req.session.flush()
    return JsonResponse({'status':'logout'})
   
    
@csrf_exempt
def register(req):
    json_data = json.loads(req.body)
    json_data['password'] = password_hash(json_data.get('password'))
    new_emp = EmployeeDetailsSerializer(data=json_data)
    
    if new_emp.is_valid():
        new_emp.save()
        return JsonResponse({"status":'added!!'})
    else:
        return JsonResponse(new_emp.errors)
    
    
@csrf_exempt
def login(req):
    json_data = json.loads(req.body)
    emp_obj=EmployeeDetails.objects.get(username=json_data['username'])
    
    if password_check(json_data.get('password'),emp_obj.password):

        return JsonResponse({'status':'Login succes'})
    else:
        return JsonResponse({'status':'login failed'})
@csrf_exempt
def update(req):
    json_data = json.loads(req.body)
    emp_obj = EmployeeDetails.objects.get(username = json_data['username'])
   
   
    json_data['password'] = password_hash(json_data.get('password'))
    updated_pass = EmployeeDetailsSerializer(emp_obj,json_data,partial=True)
    if updated_pass.is_valid():
        updated_pass.save()
        return JsonResponse({'status':'password updated'})
    else:
        return JsonResponse(updated_pass.errors)
    
def display(req):
    req.session['username'] = 'sai'
    return JsonResponse({'status':'session set'})

def sending_mail(req):
    html_content = render_to_string("main.html",{"name": "sai"}) 
    email = EmailMultiAlternatives( 
            subject="Welcome", 
            body="Welcome to our website.",  
            from_email="narishettisairam@gmail.com",
            to=["saivarma2122@gmail.com"]   
                            
    )     
    email.attach_alternative(
         
            html_content, 
            "text/html"
    )     
    email.send()     
    return HttpResponse("Email Sent") 

@csrf_exempt
def store(req):
    if 'resume' in req.FILES:
        fs = FileSystemStorage(location="media/pdf")
        fs.save(req.FILES['resume'].name,req.FILES['resume'])
        return JsonResponse({'status':'file reveied'})
    return JsonResponse({'status':'File Required'})

def show(req):
    print('iam view')
    return JsonResponse({'status':'Request reached!'})
        