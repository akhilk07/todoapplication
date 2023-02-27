from django.urls import path
from todoapp import views
urlpatterns=[
    path("signup",views.SignUpView.as_view(),name="register"),
    path("",views.LoginView.as_view(),name="signin"),
    path("home",views.IndexView.as_view(),name="index"),
    path("signout",views.SignOutView.as_view(),name="signout"),
    path("todos/add",views.TodoAddView.as_view(),name="add-todo"),
    path("todos/all",views.TodoListView.as_view(),name="todos-list")
]