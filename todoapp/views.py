from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, TemplateView, ListView,DetailView,CreateView,UpdateView
from todoapp import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from todoapp.models import Todos
from django.contrib import messages


# Create your views here.


class SignUpView(CreateView):
    model = User
    form_class = forms.RegistrationForm
    template_name = "registration.html"
    success_url = reverse_lazy("signin")

    def form_valid(self, form):
        messages.success(self.request,"Account hasbeen created")
        return super().form_valid(form)


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = forms.LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            uname = form.cleaned_data.get("username")
            pwd = form.cleaned_data.get("password")
            user = authenticate(request, username=uname, password=pwd)
            if user:
                login(request, user)

                print("login success")
                return redirect("index")
            else:
                messages.error(request, "invalid username or password")
                print("invalid credentials")
                return render(request, "login.html", {"form": form})

        return render(request, "login.html")


class IndexView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["todos"]=Todos.objects.filter(user=self.request.user,status=False)
        return context


class SignOutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("signin")


class TodoAddView(CreateView):
    model = Todos
    form_class = forms.TodoForm
    template_name = "add-todo.html"
    success_url = reverse_lazy("todos-list")

    def form_valid(self, form):
        form.instance.user=self.request.user
        messages.success(self.request,"todo has been created")
        return super().form_valid(form)


class TodoListView(ListView):
    model = Todos
    context_object_name = "todos"
    template_name = "todolist.html"

    def get_queryset(self):
        return Todos.objects.filter(user=self.request.user)



def delete_todo(request, *args, **kwargs):
    id = kwargs.get("id")
    Todos.objects.get(id=id).delete()

    return redirect("todos-list")


class TodoDetailView(DetailView):
    model = Todos
    context_object_name = "todo"
    template_name = "todo-detail.html"
    pk_url_kwarg = "id"


class TodoEditView(UpdateView):
    model = Todos
    form_class = forms.TodoChangeForm
    template_name = "todo-edit.html"
    success_url = reverse_lazy("todos-list")
    pk_url_kwarg = "id"

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "todo has been updated")
        return super().form_valid(form)
