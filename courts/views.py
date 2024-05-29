from django.shortcuts import render, get_object_or_404, redirect
from .models import Facility, Booking
from .forms import BookingForm
from django.utils import timezone
from .customer import Customer
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import logout as logouts
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q
from datetime import datetime, timedelta


def facility_list(request):
    query = request.GET.get('query', '')

    print(f"Received query: {query}")  # Debug statement

    if query:
        facilities = Facility.objects.filter(
            Q(name__icontains=query) | Q(pincode__icontains=query)
        )
        print(f"Filtered facilities: {facilities}")  # Debug statement
    else:
        facilities = Facility.objects.all()
        
    return render(request, 'facility_list.html', {'facilities': facilities})

def facility_detail(request, pk):
    facility = get_object_or_404(Facility, pk=pk)
    bookings = Booking.objects.filter(facility=facility, start_time__gte=timezone.now()).order_by('start_time')
    return render(request, 'facility_detail.html', {'facility': facility, 'bookings': bookings})



def book_facility(request, pk):
    facility = get_object_or_404(Facility, pk=pk)
    bookings = Booking.objects.filter(facility=facility)

    # Define the time slots (for example, hourly slots from 9 AM to 9 PM)
    time_slots = []
    start_time = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    end_time = datetime.now().replace(hour=21, minute=0, second=0, microsecond=0)
    current_time = start_time

    while current_time < end_time:
        slot_end_time = current_time + timedelta(hours=1)
        is_booked = bookings.filter(start_time__lt=slot_end_time, end_time__gt=current_time).exists()
        time_slots.append({
            'start_time': current_time,
            'end_time': slot_end_time,
            'is_booked': is_booked,
        })
        current_time = slot_end_time

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.facility = facility
            overlapping_bookings = Booking.objects.filter(
                facility=facility,
                start_time__lt=booking.end_time,
                end_time__gt=booking.start_time
            )
            if overlapping_bookings.exists():
                form.add_error(None, 'This time slot is already booked.')
            else:
                booking.save()
                return redirect('facility_detail', pk=pk)
    else:
        form = BookingForm()
    return render(request, 'book_facility.html', {'form': form, 'facility': facility, 'time_slots': time_slots})



def booking_list(request):
    bookings = Booking.objects.all().order_by('start_time')
    return render(request, 'booking_list.html', {'bookings': bookings})

def signup(request):
    if request.method=='GET':
        return render(request,'signup.html')
    else:
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        mobile=request.POST['mobile']
        email=request.POST['email']
        password=request.POST['password']
        password=make_password(password)
        userdata=[first_name,last_name,mobile,email,password]
        print(userdata)

        #storing object
        customerdata=Customer(first_name=first_name,last_name=last_name,mobile=mobile,email=email,password=password)
        #validation
        error_msg=None
        success_msg=None
        
        if(not first_name):
            error_msg="First Name Required !"
        elif(not last_name):
            error_msg="Last Name Required !"
        elif(not mobile):
            error_msg="Mobile Number Required !"
        elif(not email):
            error_msg="Email Required !"
        elif(not password):
            error_msg="Password Required !"
        elif(customerdata.isexist()):
            error_msg='Email Already Exists'
        if (not error_msg):
            success_msg="Account Created Successfully"
            customerdata.save()
        msg={'error':error_msg,'success':success_msg}
        return render(request,'signup.html',msg)


def login(request):
    if request.method=='GET':
        return render(request,'login.html')
    else:
        email=request.POST['email']
        password=request.POST['password']
        #to check email found or not
        users=Customer.getemail(email)
        error_msg=None
        if users:
            check=check_password(password,users.password)
            #if password found
            if check:
                return redirect('/')
            else:
                error_msg='password is incorrect'
                msg={'error':error_msg}
                return render(request,'login.html',msg)
        else:
            error_msg='email is incorrect'
            msg={'error':error_msg}
            return render(request,'login.html',msg)

def logout(request):
    if request.method=='POST':
        logouts(request)
        return redirect('home')
    else:
        return render(request,'logout.html')

