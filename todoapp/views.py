from django.shortcuts import render,redirect
from django.views.generic import View,TemplateView
from todoapp import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from todoapp.models import Todos

# Create your views here.


class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=forms.RegistrationForm()
        return render(request,"registration.html",{"form":form})

    def post(self,request,*args,**kwargs):
        form=forms.RegistrationForm(request.POST)
        if form.is_valid():

            User.objects.create_user(**form.cleaned_data)
            return redirect("signin")
        return render(request,"registration.html")

class LoginView(View):
    def get(self,request,*args,**kwargs):
        form=forms.LoginForm()
        return render(request,"login.html",{"form":form})

    def post(self,request,*args,**kwargs):
        form=forms.LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user=authenticate(request,username=uname,password=pwd)
            if user:
                login(request, user)

                print("login success")
                return redirect("index")
            else:
                print("invalid credentials")
                return render(request,"login.html",{"form":form})

        return render(request,"login.html")

class IndexView(TemplateView):
    def get(self,request,*args,**kwargs):
        return render(request,"home.html")

class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")

class TodoAddView(View):
    def get(self,request,*args,**kwargs):
        form=forms.TodoForm()
        return render(request,"add-todo.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=forms.TodoForm(request.POST)
        if form.is_valid():

            form.instance.user=request.user
            form.save()
            return redirect("index")
        else:
            return render(request,"add-todo.html",{"form":form})

class TodoListView(View):
    def get(self,request,*args,**kwargs):
        all_todos=Todos.objects.filter(user=request.user)
        return render(request,"todolist.html",{"form":all_todos})