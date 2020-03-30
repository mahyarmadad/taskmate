from django.shortcuts import render, redirect
from django.http import HttpResponse
from firstapp.models import TaskList
from firstapp.form import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def todolist(request):
    if request.method == "POST":
        form = TaskForm(request.POST or None)
        if form.is_valid():
            form.save(commit=False).manage = request.user
            form.save()
            messages.success(request,("New Task Added!"))
            return redirect("todolist")
        
    else:
        alltask = TaskList.objects.filter(manage=request.user)
        paginater = Paginator(alltask,10)
        page = request.GET.get("page")
        alltask = paginater.get_page(page)
    return render(request,"todolist.html", {"alltask":alltask})

@login_required
def delete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.manage == request.user:
        task.delete()
    else:
        messages.error(request,"Access Denied!")
    
    return redirect("todolist")


@login_required
def edit_task(request, task_id):
    if request.method == "POST":
        task = TaskList.objects.get(pk=task_id)
        form = TaskForm(request.POST or None, instance = task)
        if form.is_valid():
            form.save()
            messages.success(request,("Task Edited!"))
            return redirect("todolist")
    
    else:
        task_obj = TaskList.objects.get(pk=task_id)
    return render(request,"edit.html", {"task_obj":task_obj})

@login_required
def complete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.manage == request.user:
        task.done = True
        task.save()
    else:
        messages.error(request,"Access Denied!")
    return redirect("todolist")

@login_required
def pending_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.manage == request.user:
        task.done = False
        task.save()
    else:
        messages.error(request,"Access Denied!")
    return redirect("todolist")

def about(request):
    context = {"aboutxt":"Welcom from about"}
    return render(request,"about.html", context)

def content(request):
    context = {"contettxt":"Welcom from content"}
    return render(request,"content.html", context)

def index(request):
    context = {"indextxt":"Welcom from Home/Index"}
    return render(request,"index.html", context)


