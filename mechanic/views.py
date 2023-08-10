from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .models import *
from site_admin.models import *
from django.core.files.storage import FileSystemStorage
from public.models import Registration as User_Registration, Complaints as User_Complaints, Messages as User_Messages

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
                    request.session['usertype'] = 'mechanic_user'
                    return redirect(reverse('mechanic:dashboard'))
                else:
                    messages.error(request, 'User is suspended. Contact the admin!')
                    return redirect(reverse('mechanic:signin'))
            else:
                messages.error(request, 'Invalid credentials!')
                return redirect(reverse('mechanic:signin'))
    return render(request,'mechanic/signin.html')

def signup(request):
    if request.method == 'POST':
        data_record = request.POST
        uploaded_file = request.FILES['change_avatar']
        fs = FileSystemStorage()
        file_name = fs.save("PROFILE_"+uploaded_file.name, uploaded_file)
        if Registration.objects.filter(email=data_record['email_address']):
            messages.error(request, 'Email already exists! Please try again!')
            return redirect(reverse('mechanic:signup'))
        elif Registration.objects.filter(mobilenumber=data_record['mobilenumber']):
            messages.error(request, 'Mobile number already exists! Please try again!')
            return redirect(reverse('mechanic:signup'))
        else:
            registration = Registration(
            firstname=data_record['firstname'],
            lastname=data_record['lastname'],
            email=data_record['email_address'],
            mobilenumber=data_record['mobilenumber'],
            address=data_record['address'],
            password=data_record['password'],
            location=Location.objects.filter(unique_id=data_record['location_list']).get(),
            about_me=data_record['about_me'],
            my_skills=data_record['my_skills'],
            profile_image=fs.url(file_name),
            status='active',
            )
            registration.save()
            messages.success(request, 'mechanic user registered successfully!')
            return redirect(reverse('mechanic:signin'))
    loaction_list = Location.objects.all()
    context = { 'loaction_list' : loaction_list }
    return render(request,'mechanic/signup.html', context)

def logout(request):
    del request.session['is_logged_in']
    del request.session['firstname']
    del request.session['lastname']
    del request.session['email']
    del request.session['user_id']
    del request.session['mobilenumber']
    del request.session['usertype']
    return redirect(reverse('mechanic:signin'))

def dashboard(request):
    return render(request,'mechanic/dashboard.html')

def complaints_list(request):
    complaints_list = User_Complaints.objects.filter(selected_mechanic=Registration.objects.get(unique_id=request.session['user_id'])).all()
    context = { 'complaints_list': complaints_list }
    return render(request, 'mechanic/complaints-list.html', context)

def complaints_view(request, id):
    complaints = User_Complaints.objects.filter(unique_id=id,status='open').get()
    if request.method == 'POST':
        data_record = request.POST
        complaints.reply = data_record['reply']
        complaints.status = data_record['change_status']
        complaints.save()

        if data_record['change_status'] != 'closed':
            messages.success(request, 'Replied successfully!')
            return redirect(reverse('mechanic:complaints_views', args=[id]))
        else:
            messages.success(request, 'Replied successfully!')
            return redirect(reverse('mechanic:complaints_list'))
    user_id = complaints.public_user.unique_id
    user_messages = User_Messages.objects.filter(complaints=User_Complaints.objects.filter(unique_id=id).get()).all()
    context = { 'userdata' : User_Registration.objects.get(unique_id=user_id), 'complaints': complaints, 'user_messages': user_messages, 'complaint_id': id, 'user_id':user_id }
    return render(request, 'mechanic/complaints-view.html', context)

def add_messages(request, id, id2):
    if request.method == 'POST':
        data_record = request.POST
        mess_app= User_Messages(
        messages_text=data_record['message'],
        complaints=User_Complaints.objects.get(unique_id=id),
        mechanic_user_id=request.session['user_id'],
        public_user_id=id2,
        status=request.session['usertype'],
        )
        mess_app.save()
        messages.success(request, 'Added')
    return redirect(reverse('mechanic:complaints_views', args=[id]))
