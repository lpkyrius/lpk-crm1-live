from django.http import HttpResponse
from django.shortcuts import redirect

'''
decorator uma função que toma outra função como parâmetro
e permite incluir mais funcionalidades antes da outra função ser chamada

exemplo: --------------
@unauthenticator_user
def loginPage(request):
-----------------------
na chamada acima, LoginPage(request) será passada para
o decorator @unauthenticator_user como parâmetro

'''

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('Você não está autorizado a visualizar esta página')
        return wrapper_func
    return decorator

def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'customer':
            return redirect('user-page')

        if group == 'admin':
            return view_func(request, *args, **kwargs)

    return wrapper_function

