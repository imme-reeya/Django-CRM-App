from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import record

# Create your views here.
def home(request):
    records = record.objects.all()

    # check if they are logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password. Please Try Again..")
            return redirect('home')
    else:
         return render(request, 'home.html', {'Records': records})

def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out..")
    return redirect('home')

def register_user(request):

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and Login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request,"You Have Been Registered Successfully!Welcome!!")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html',{'form':form})

    return render(request, 'register.html',{'form':form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = record.objects.get(id=pk)
        return render(request, 'customer_record.html',{'customer_record':customer_record})
    else:
        messages.error(request,"Login to access the data")
        return redirect('home')

def delete_record(request,pk):
    if request.user.is_authenticated:
        delete_it = record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request,"Customer Record Deleted Successfully")
        return redirect('home')
    else:
        messages.error(request,"Login to access the data")
        return redirect('home')

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request,"Record Added Successfully")
                return redirect ('home')
        return render(request, 'add_record.html',{'form':form})
    else:
        messages.error(request,"You Must Be Logged In..")
        return redirect('home')

def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request,"Record Has Been Updated!")
            return redirect('home')
        return render(request, 'update_record.html',{'form':form})
    else:
        messages.error(request,"You Must Be Logged In..")
        return redirect('home')

         







