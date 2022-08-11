from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from blog.models import Post
from .models import Contact
from django.contrib import messages

# Create your views here.

# HTML Pages
def home(request):
    latest = Post.objects.latest('timeStamp')
    context = {'latest': latest}
    return render(request, 'home/home.html', context)

def about(request):
    return render(request, 'home/about.html')

def contact(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        content = request.POST["content"]
        contact = Contact(name=name, email=email, phone=phone, content=content)
        contact.save()
        messages.success(request, "Your request submitted successfully!")
        return redirect("home")

    return render(request, 'home/contact.html')

def write(request):
    if request.method == "POST":
        title = request.POST["title"]
        author = request.POST["author"]
        content = request.POST["content"]
        slug = ("-".join(title.split())).lower()
        print(title, author, content, slug)
        posts = Post(title=title, author=author, content=content, slug=slug)
        posts.save()
        messages.success(request, "Post added successfully!")
        return redirect('home')
    return render(request, 'home/write.html')

def search(request):
    query = request.GET["query"]
    allPostsTitle = Post.objects.filter(title__icontains=query)
    allPostsContent = Post.objects.filter(content__icontains=query)
    allPostsUni = allPostsTitle.union(allPostsContent)
    allPostsAuthor = Post.objects.filter(author__icontains=query)
    allPosts = allPostsUni.union(allPostsAuthor)
    context = {'allPosts': allPosts, 'query': query}
    return render(request, 'home/search.html', context)

# Authentication APIs
def handleSignup(request):
    if request.method == "POST":
        # Get the post parameters
        username = request.POST["username"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]

        # Check for errorneous inputs
        if not username.isalnum() or len(username) > 10:
            messages.error(request, 'Your username should be alphanumeric and less than 10 characters!')
            return redirect("home")

        if pass1 != pass2:
            messages.error(request, 'Passwords did not match!')
            return redirect("home")

        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()

        messages.success(request, "Account created, Now you can log in to your account!")
        return redirect("home")
    return render(request, "home/signup.html")

def handleLogin(request):
    if request.method == "POST":
        # Get the post parameters
        loginusername = request.POST["loginusername"]
        loginpassword = request.POST["loginpassword"]

        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in!")   
            return redirect("home")
        else:
            messages.error(request, "Invalid Credentials!")
            return redirect("home")
        
    return render(request, "home/login.html")

def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out!")
    return redirect("home")