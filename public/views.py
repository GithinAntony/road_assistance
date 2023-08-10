from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .models import *
from mechanic.models import Registration as Mechanic_Registration
from site_admin.models import *

# Create your views here.
def signin(request):
    if request.method == 'POST':
            data_record = request.POST
            if Registration.objects.filter(mobilenumber=data_record['mobilenumber'],password=data_record['password']):
                user_details = Registration.objects.get(mobilenumber=data_record['mobilenumber'],password=data_record['password'])
                if user_details.status == 'active':
                    request.session['is_logged_in'] = True
                    request.session['email'] = user_details.email
                    request.session['firstname'] = user_details.firstname
                    request.session['lastname'] = user_details.lastname
                    request.session['user_id'] = user_details.unique_id
                    request.session['mobilenumber'] = user_details.mobilenumber
                    request.session['usertype'] = 'user'
                    return redirect(reverse('public:dashboard'))
                else:
                    messages.error(request, 'User is suspended. Contact the admin!')
                    return redirect(reverse('public:signin'))
            else:
                messages.error(request, 'Invalid credentials!')
                return redirect(reverse('public:signin'))
    return render(request,'public/signin.html')

def signup(request):
    if request.method == 'POST':
        data_record = request.POST
        if Registration.objects.filter(email=data_record['email_address']):
            messages.error(request, 'Email already exists! Please try again!')
            return redirect(reverse('public:signup'))
        elif Registration.objects.filter(mobilenumber=data_record['mobilenumber']):
            messages.error(request, 'Mobile number already exists! Please try again!')
            return redirect(reverse('public:signup'))
        else:
            registration = Registration(
            firstname=data_record['firstname'],
            lastname=data_record['lastname'],
            email=data_record['email_address'],
            mobilenumber=data_record['mobilenumber'],
            address=data_record['address'],
            password=data_record['password'],
            status='active',
            )
            registration.save()
            messages.success(request, 'public user registered successfully!')
            return redirect(reverse('public:signin'))
    return render(request,'public/signup.html')

def logout(request):
    del request.session['is_logged_in']
    del request.session['firstname']
    del request.session['lastname']
    del request.session['email']
    del request.session['user_id']
    del request.session['mobilenumber']
    del request.session['usertype']
    return redirect(reverse('public:signin'))

def dashboard(request):
    return render(request,'public/dashboard.html')

def search_mechanic(request):
    mechanic_list = Mechanic_Registration.objects.all()
    if request.method == 'POST':
        data_record = request.POST
        mechanic_list = Mechanic_Registration.objects.filter(location=Location.objects.get(unique_id=data_record['location_list'])).all()
    loaction_list = Location.objects.all()
    category_list = Category.objects.all()
    context = { 'loaction_list' : loaction_list, 'category_list': category_list, 'datalist': mechanic_list }
    return render(request,'public/search-mechanic.html',context)

def search_mechanic_view(request, id):
    if request.method == 'POST':
        data_record = request.POST
        complaints = Complaints(
        complaints_text=data_record['complaint'],
        location_text=data_record['location'],
        selected_mechanic=Mechanic_Registration.objects.filter(unique_id=id).get(),
        public_user=Registration.objects.filter(unique_id=request.session['user_id']).get(),
        status='open',
        )
        complaints.save()
        messages.success(request, 'Complaints added!')
        return redirect(reverse('public:search_mechanic_view', args=[id]))
    get_complaints = Complaints.objects.filter(public_user=Registration.objects.filter(unique_id=request.session['user_id']).get(),selected_mechanic=Mechanic_Registration.objects.filter(unique_id=id).get(),status='open').all()[:1]

    complaint_id = 0
    for i in get_complaints:
        complaint_id = i.unique_id
    if complaint_id > 0:
       user_messages = Messages.objects.filter(complaints=Complaints.objects.filter(unique_id=complaint_id,status='open').get()).all()
    else:
        user_messages = ''
    context = { 'userdata' : Mechanic_Registration.objects.get(unique_id=id), 'get_complaints' : get_complaints, 'complaint_id': complaint_id, 'mechanic_id': id, 'user_messages': user_messages }
    return render(request,'public/search-mechanic-view.html', context)

def add_messages(request, id, id2):
    if request.method == 'POST':
        data_record = request.POST
        mess_app = Messages(
        messages_text=data_record['message'],
        complaints=Complaints.objects.filter(unique_id=id).get(),
        mechanic_user_id=id2,
        public_user_id=request.session['user_id'],
        status=request.session['usertype'],
        )
        mess_app.save()
        messages.success(request, 'Added')
    return redirect(reverse('public:search_mechanic_view', args=[id2]))
