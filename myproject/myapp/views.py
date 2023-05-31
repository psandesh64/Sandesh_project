from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Todo,Users_image

# Create your views here.
def home(request):
    return render(request,'home.html',{})

@login_required
def todo(request):
    user = request.user
    todos = Todo.objects.filter(user=user)
    if request.method == 'POST':
        todo_list = request.POST['todo_list']
        task = Todo(todo_list=todo_list,user=user)
        task.save()
        return render(request,'todo.html',{'todos':todos})
    
    return render(request,'todo.html',{'todos':todos})

@login_required
def todoedit(request,id):
    user = request.user
    key=int(id)
    todos = Todo.objects.filter(user=user)
    todo_list_prev = Todo.objects.filter(id=key, user=user).first()
    if request.method == 'POST':
        todo_list = request.POST['todo_list']
        status = request.POST.get('status')
        if status=="true":
            status=True
        else:
            status=False
        if todo_list:
            task = Todo(id=key,todo_list=todo_list,user=user,status=status)
            task.save()
        else:
            todo_list=todo_list_prev.todo_list
            task = Todo(id=key,todo_list=todo_list,user=user,status=status)
            task.save()
        return redirect('todo')

    return render(request,'todoedit.html',{'todos':todos,'key':key})

@login_required
def tododelete(request,id):
    user = request.user
    key=int(id)
    Todo.objects.filter(id=key,user=user).delete()
    return redirect('todo')

def images(request):
    return render(request,'images.html',{})

def handlelogin(request):
    if request.method == 'POST':
        loginusername = request.POST['username']
        loginpassword = request.POST['password']

        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request,user)
            messages.success(request,"Successfully Logged In")
            return redirect('home')
        else:
            return HttpResponse('404 - Not Found')

def handlelogout(request):
    logout(request)
    messages.success(request,"Successfully Logged Out")
    return redirect('home')

def handlesignup(request):
    if request.method == 'POST':
        username=request.POST['username']
        pass1=request.POST['password1']
        pass2=request.POST['password2']
        checkuser=User.objects.filter(username=username)
        print(checkuser)
        # check for errorneous inputs:

        # length of username
        if len(username)>15:
            messages.error(request,"Username must be under 15 characters")
            return redirect('home')
        
        # username should be alphanumeric
        if not username.isalnum():
            messages.error(request,"Username must only contain letter and numbers")
            return redirect('home')
        
        # password should match
        if pass1!=pass2:
            messages.error(request,"Password do not match")
            return redirect('home')
        
         # Unique User
        if checkuser.exists():
            messages.error(request,"User Already exist")
            return redirect('home')
        
        else:
        # creat user
            email=None
            myuser = User.objects.create_user(username,email,pass1)
            myuser.save()
            messages.success(request, "Your account has been successfully created")
            return redirect('home')
        
@login_required
def image_page(request):
    user=request.user
    imagedata = Users_image.objects.filter(user=user)
    if request.method == 'POST':
        photo = request.FILES['photo']
        name = request.POST.get('name')
        profile = Users_image.objects.create(user=user,photo=photo,name=name)
        profile.save()
        return render(request,'imageupload.html',{'imagedata':imagedata})
    return render(request,'imageupload.html',{'imagedata':imagedata})

@login_required
def image_del_page(request):
    user = request.user
    imagedata = Users_image.objects.filter(user=user)
    if request.method == 'POST':
        image_ids = request.POST.getlist('image_ids')  # Get the selected image IDs as a list
        for image_id in image_ids:
            Users_image.objects.filter(id=image_id, user=user).delete()  # Delete the selected images
        
        return redirect('images')
    
    return render(request, 'imagedelete.html', {'imagedata': imagedata})
