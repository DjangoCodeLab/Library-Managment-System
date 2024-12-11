import requests
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from App.models import *
from functools import wraps
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.



def home(request):
    queryset = Book.objects.all()
    total_count= queryset.count()
    percentage_of_stock = ((total_count/total_count) * 100)
    return render(request, 'home.html',{'queryset':percentage_of_stock})



@login_required(login_url='/login')

def products(request):
    # Initialize filters
    filters = {}
    books = Book.objects.all()  # Start with all books

    # Fields to filter by
    fields = ['book_id', 'title', 'author', 'language_code', 'publication_date', 'publisher']
    for field in fields:
        value = request.GET.get(field,'').strip()
        if value or value == '':
            filters[f"{field}__icontains"] = value

    # Apply filters
    if filters:
        books = books.filter(**filters)

    # Apply price filter
    price = request.GET.get('price')
    if price:
        if price == "1":
            books = books.filter(price__gte=100, price__lte=250)
        elif price == "2":
            books = books.filter(price__gte=250, price__lte=500)
        elif price == "3":
            books = books.filter(price__gte=500, price__lte=750)
        elif price == "4":
            books = books.filter(price__gte=750, price__lte=1000)

    # Apply average rating filter
    aveRate = request.GET.get('average_rating')
    if aveRate:
        if aveRate == "1":
            books = books.filter(average_rating__gte=2, average_rating__lte=3)
        elif aveRate == "2":
            books = books.filter(average_rating__gte=3, average_rating__lte=4)
        elif aveRate == "3":
            books = books.filter(average_rating__gte=4, average_rating__lte=5)

    # Apply sorting
    dataFilter = request.GET.get('dataFilter')
    if dataFilter:
        if dataFilter == "low":
            books = books.order_by('price')
        elif dataFilter == "high":
            books = books.order_by('-price')
        elif dataFilter == "AtoZ":
            books = books.order_by('title')
        elif dataFilter == 'ZtoA':
            books = books.order_by('-title')

    # Paginate after filtering and sorting
    paginator = Paginator(books, 5)  # 5 books per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    
    # Prepare context and render
    context = {
        'books': page_obj,
        
        }
    return render(request, 'products.html', context)


def login_user(request):
    data = request.POST

    if(request.method == 'POST'):
        username = data.get('username')
        password = data.get('password')

        if not User.objects.filter(username=username).exists():
            messages.warning(request, "username is not exists")
            return redirect('/register')
        
        user = authenticate(username = username, password = password)
        

        if user is None:
            messages.warning(request, "password is invalid")
            return redirect('/login')
        
        else:
            login(request,user)
            return redirect('/')
        
        
   
    return render(request, 'login.html')

def register_user(request):
    data = request.POST
    if request.method == "POST":
        first_name = data.get('first_name','').strip()
        last_name = data.get('last_name','').strip()
        email = data.get('email','').strip()
        username = data.get('username','').strip()
        password = data.get('password','').strip()

        if not all([first_name,last_name,email,username,password]):
            messages.warning(request,"All fields are required")
            return redirect('/register')
        
        if(User.objects.filter(username = username).exists()):
            messages.warning(request, "Username Already Exists")
            return redirect('/register')
        
        if(User.objects.filter(email = email).exists()):
            messages.warning(request, "Email Already Exists!")
            return redirect('/register')
        
        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username=username,
            email = email,
        )
        user.set_password(password)
        user.save()
        # Automatically create a profile for the user


        if not Profile.objects.filter(user=user).exists():
            Profile.objects.create(user=user) 

        return redirect('/login')
    
    return render(request, 'register.html')


def logout_user(request):
    logout(request)
    return redirect('/login')

@login_required
def profile(request):
    profile = request.user.profile 
    return render(request, 'profile.html',{'profile':profile})


@login_required(login_url='/login')
def edit_profile(request):
    profile = request.user.profile 
     
    if request.method == "POST":
        bio = request.POST.get('bio','').strip()
        role = request.POST.get('role','').strip()
        profile_picture = request.FILES.get('profile_picture')


        if not bio:
            messages.warning(request,"Bio cannot be empty")
            return redirect('edit_profie')
        profile.bio = bio
        profile.role = role if role else profile.role 

        if profile_picture:
            profile.profile_picture = profile_picture
        profile.save()
        print("Bio:", bio)
        print("Role:", role)
        print("Profile Picture:", profile_picture)
        messages.success(request,'profile updated successfully')
        return redirect('profile')
    return render(request,'edit_profile.html',{'profile':profile})



def update_book(request,id):
    book = Book.objects.get(id = id)
    if request.method == "POST":
        title = request.POST.get('title')
        author = request.POST.get('author')
        publisher = request.POST.get('publisher')
        price = request.POST.get('price')

        book.title = title
        book.author = author
        book.publisher = publisher
        book.price = price 
        book.save()
        messages.success(request, "updated Successfully")
        return redirect('/')

    context = {
        'book':book
    }
    return render(request, 'update.html',context)


def delete(request,id):
    book = Book.objects.get(id = id)
    book.delete()
    messages.info(request, "Data Sucessfully delete")
    return redirect('/products')

