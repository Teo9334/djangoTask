
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from .models import Task

# REEDIRECCIONAR
def redirecting(request):
    # Comprobar si está registrado, llevarlo a home
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return redirect('login')

# LOGIN
def login_user(request):
    # Comprobar si está registrado, llevarlo a home
    if request.user.is_authenticated:
        return redirect("home")
    else:
        # COMPROBAR SI EL USUARIO EXISTE
        if request.method == "POST":
            user = authenticate(request, username=request.POST['user'], password=request.POST['password'])
            if user is None:
                msg = "Usuario o contraseña incorrectos..."
                return render(request, 'login.html', {"error" : msg})
            else:
                login(request, user)
                return redirect("home")
        else:   
            return render(request, 'login.html')

# REGISTER
def register_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            # COMPROBAR SI EL USUARIO YA EXISTE
            user = User.objects.filter(username=request.POST['user'])
            if user.exists():
                msg = "El usuario ya existe"
                return render(request, 'register.html', {'error' : msg})
            else:
                # COMPROBAR QUE LAS CONTRASEÑAS SEAN IGUALES
                if request.POST['password1'] == request.POST['password2']:
                    user = User.objects.create_user(username=request.POST['user'], password=request.POST['password1'])
                    login(request, user)
                    return redirect('home')
                else:
                    msg = "Las contraseñas no son iguales"
                    return render(request, 'register.html', {'error' : msg})
        else:
            return render(request, 'register.html')

# CERRAR SESIÓN
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')

# HOME
def home(request):
    # Comprobar si está registrado, llevarlo a home
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user)
        
        return render(request, 'home.html', { "ide" : "home", "tasks" : tasks})
    else: 
        return redirect('login')

# Task Realizadas
def taskRealizadas(request):
    # Comprobar si está registrado, llevarlo a home
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user)
        
        return render(request, 'taskRealizadas.html', { "ide" : "taskRealizadas", "tasks" : tasks})
    else: 
        return redirect('login')

# Task Pendientes
def taskPendientes(request):
    # Comprobar si está registrado, llevarlo a home
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user)
        
        return render(request, 'taskPendientes.html', { "ide" : "taskPendientes", "tasks" : tasks})
    else: 
        return redirect('login')


# PROFILE
def profile(request):
    # Comprobar si está registrado, llevarlo a home
    if request.user.is_authenticated:
        user = request.user
        return render(request, 'profile.html', { "ide" : "profile", "user" : user})
    else: 
        return redirect('login')

# EDITAR PERFIL
def editProfile(request, id):
    # Comprobar que el usuario esté autenticado
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=id)
        
        # Comprobar si es el usuario logeado
        if user.id == request.user.id:
            
            if request.method == "POST":
                newName = request.POST['newName']
                passwordOld = request.POST['passwordOld']
                
                # Comprobar que la contraseña vieja sea correcta
                if user.check_password(passwordOld):
                    # Comprobar que las contraseñas nuevas coincidan
                    if request.POST['passwordNew1'] == request.POST['passwordNew2']:
                        
                        # Actualizar usuario
                        user.username = newName
                        user.set_password(request.POST['passwordNew1'])
                        user.save()
                        
                        # Actualizar sesión de user
                        update_session_auth_hash(request, user)
                        
                        return redirect('profile')
                    else:
                        msg = "Las contraseñas no coinciden"
                        return render(request,'editPerfil.html', { "error" : msg})
                else:
                    msg = "La contraseña anterior es incorrecta"
                    return render(request,'editPerfil.html', { "error" : msg})
                
            else:
                return render(request,'editPerfil.html')
        else:
            return redirect('home')
    else:
            return redirect('login')

# Elminiar perfil
def deleteProfile(request, id):
    # Comprobar si está registrado, llevarlo a home
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=id)
        
        # Comprobar si es el usuario logeado
        if user.id == request.user.id:
            if request.method == "POST":
                # Comprobar si las contraseñas coinciden
                if request.POST['password1'] == request.POST['password2']:
                    # Comprobar que la contraseña sea la correcta
                    if user.check_password(request.POST['password1']):
                        # Eliminar usuario
                        user.delete()
                        return redirect("login")
                    else:
                        msg = "Las contraseña es incorrecta"
                        return render(request, 'deletePerfil.html', { "ide" : "profile", "user" : user, 'error' : msg})    
                else:
                    msg = "Las contraseñas no coinciden"
                    return render(request, 'deletePerfil.html', { "ide" : "profile", "user" : user, 'error' : msg})
            else:
                return render(request, 'deletePerfil.html', { "ide" : "profile", "user" : user})
        else:
            return redirect('home')
    else: 
        return redirect('login')

# AÑADIR TAREA
def add_task(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            # Obtener el usuario actual
            user = request.user
            
            # Obtener los datos de la Tarea
            checkbox = False
            title = request.POST['title']
            description = request.POST['texto']
            endDate = request.POST['endDate']
            
            # Comprobar si se marcó el checkbox
            if request.POST.get('checkbox') == '1':
                checkbox = True
            
            # Crear tarea
            new_task = Task(user=user, title=title, description=description,endDate=endDate, complete=checkbox)
        
            new_task.save()
        
            return redirect('home')
        else:
            return render(request,'addTask.html',{ "ide" : "añadir"})
        
    else:
        return redirect('login')

# Ver Tarea
def taskView(request, id):
    # Comprobar que el usuario esté autenticado
    if request.user.is_authenticated:
        task = get_object_or_404(Task, id=id)
        # Comprobar si el id pertenece al usuario 
        if task.user == request.user:
            return render(request, 'verTarea.html', {'task' : task})
        else:
            return redirect('home')
    else:
            return redirect('login')

# Actualizar task complete
def taskComplete(request, id):
    # Comprobar que el usuario esté autenticado
    if request.user.is_authenticated:
        task = get_object_or_404(Task, id=id)
        # Comprobar si el id pertenece al usuario 
        if task.user == request.user:
            
            # Negar task.complete
            task.complete = not(task.complete)
            task.save()
            
            return redirect('taskView', id=task.id)
        else:
            return redirect('home')
    else:
            return redirect('login')

# Editar Task
def editTask(request, id):
    # Comprobar que el usuario esté autenticado
    if request.user.is_authenticated:
        task = get_object_or_404(Task, id=id)
        # Comprobar si el id pertenece al usuario 
        if task.user == request.user:
            if request.method == "POST":
                task.title = request.POST["title"]
                task.description = request.POST["texto"]
                task.endDate = request.POST['endDate']
                task.save()
                
                return redirect('taskView', id=task.id)
            else:
                return render(request, 'editTask.html', {"task" : task })
        else:
            return redirect('home')
    else:
        return redirect('login')

# Eliminar Task
def deleteTask(request, id):
    # Comprobar que el usuario esté autenticado
    if request.user.is_authenticated:
        task = get_object_or_404(Task, id=id)
        # Comprobar si el id pertenece al usuario 
        if task.user == request.user:
            task.delete()
            return redirect('home')
        else:
            return redirect('home')
    else:
        return redirect('login')