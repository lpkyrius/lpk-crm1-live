from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

#pdf
from django.template.loader import render_to_string
from django.db.models import Sum
from django.conf.urls.static import static

# Create your views here.
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only

from plotly.offline import plot
import plotly.graph_objects as go

#pdf
from weasyprint import HTML
import tempfile
import os
import datetime
import static

@unauthenticated_user
def registerPage(request):

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Conta criada para ' + username)

            return redirect('login')

    context = {'form':form}
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):

    # pega os valores durante o login | de forma segura através do csrf_token
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')
        # autenticando o usuário
        user = authenticate(request, username=username, password=password)
        # se realmente autenticou
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Usuário ou Senha incorreta')

    context = {}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

# exige usuário logado
@login_required(login_url='login')
#@admin_only # somente usuários do grupo 'admin' podem acessar a home | posso ampliar para outros grupos ['admin','staff']
@allowed_users(allowed_roles=['admin','customer'])
def home(request):

    # Customer visualiza somente seus próprios pedidos
    if request.user.groups.all()[0].name == 'customer':
        orders = Order.objects.filter(customer=request.user.customer.id)
        customers = Customer.objects.filter(id=request.user.customer.id)
        #print('request name =' + request.user.name)
        #print('order=' + str(order.customer))
        #print('customer=' + str(customers.name))
    else:
        orders = Order.objects.all()
        customers = Customer.objects.all()

    #print('request.user.id ' + str(request.user.id))


    #orders = Order.objects.all()
    #customers = Customer.objects.all()

    total_customers = customers.count()

    total_orders = orders.count()
    delivered = orders.filter(status='Entregue').count()
    pending = orders.filter(status='Pendente').count()

    context = {'orders':orders, 'customers':customers,
    'total_orders':total_orders,'delivered':delivered,
    'pending':pending }

    return render(request, 'accounts/dashboard.html', context)

# exige usuário logado
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer']) # somente usuários do grupo 'customer' podem acessar a home | posso ampliar para outros grupos ['admin','staff']
def userPage(request):
    orders = request.user.customer.order_set.all() # porque os pedidos ser referem ao customer e não ao user

    total_orders = orders.count()
    delivered = orders.filter(status='Entregue').count()
    pending = orders.filter(status='Pendente').count()

    #print('PEDIDOS:', orders)

    context = {'orders':orders,'total_orders':total_orders,
    'delivered':delivered, 'pending':pending }
    return render(request, 'accounts/user.html', context)


# exige usuário logado
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','customer']) # configurações para usuários comuns
def accountSettings(request):
    # peaa as informações do customer vincluado ao user atual (nesse formato por conta do relacionamento que definimos entre as tabelas)
    customer = request.user.customer
    form = CustomerForm(instance=customer) #herda o form padrão e exibe com informações da instância atual

    if request.method == 'POST':
        # request.FILES para enviar tambem os arquivos como a foto do perfil
        form = CustomerForm(request.POST, request.FILES,  instance=customer)
        if form.is_valid():
            form.save()

    context = {'form':form}
    return render(request, 'accounts/account_settings.html', context)


# exige usuário logado
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin']) # somente usuários do grupo 'admin' podem acessar a home | posso ampliar para outros grupos ['admin','staff']
def products(request):
    products = Product.objects.all()

    return render(request, 'accounts/products.html', {'products':products})


# exige usuário logado
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','customer']) # ajustar para que se não for admin, veja apenas as próprias ordens
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)

    #print('request.user.customer.id ' + str(request.user.id))

    if request.user.groups.all()[0].name == 'customer' and request.user.customer.id != customer.id:
        return HttpResponse('Você não está autorizado a visualizar esta página')

    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer':customer, 'orders':orders, 'order_count':order_count,
    'myFilter':myFilter}
    return render(request, 'accounts/customer.html',context)


# exige usuário logado
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','customer'])
def createOrder(request, pk):
    # extra=5 para criar 5 linhas de cada vez
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=5 )
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
    #form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        #print('Printing POST:', request.POST)
        form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'form':formset}
    return render(request, 'accounts/order_form.html', context)


# exige usuário logado
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','customer'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    print('ORDER:', order)
    if request.method == 'POST':

        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'accounts/order_form.html', context)


# exige usuário logado
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','customer'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')

    context = {'item':order}
    return render(request, 'accounts/delete.html', context)

'''
class AssessView(TemplateView):
    template_name = 'chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"] = Club.objects.all()
        return context
'''

# To render the graph to a plotly graph (gráfico cinza)
def assessview(request):
    def scatter():
        x1 = [1,2,3,4]
        y1 = [30, 35, 25, 45]

        trace = go.Scatter(
            x=x1,
            y = y1
        )
        layout = dict(
            title='Gráfico Simples',
            xaxis=dict(range=[min(x1), max(x1)]),
            yaxis = dict(range=[min(y1), max(y1)])
        )

        fig = go.Figure(data=[trace], layout=layout)
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div

    context ={'plot_1': scatter()}

    return render(request, 'result_assess.html', context)


# Export to PDF
def export_pdf(request):

    print('vou exibir request')
    print(request)

    response = HttpResponse(content_type='application/pdf')

    # download direto
    #response['Content-Disposition'] = 'attachment; filename=Assessment1' + str(datetime.datetime.now()) + '.pdf'

    # abrir em nova aba do navegador
    response['Content-Disposition'] = 'inline; attachment; filename=Assessment1' + str(datetime.datetime.now()) + '.pdf'

    response['Content-Transfer-Encoding'] = 'binary'

    html_string = render_to_string('painel.html')
    #html_string = render_to_string('result_assess.html',{})
    html = HTML(string=html_string)

    result =  html.write_pdf()

    # escrevendo o pdf na memória antes de abrirmos ou realizarmos o download
    with tempfile.NamedTemporaryFile(delete=False) as output:

        output.write(result)
        output.flush()
        output=open(output.name,'rb') #Abrir como leitura "r" o arquivo binário "b""
        response.write(output.read())

    return response



def painel(request):

    return render(request, 'painel.html', {})

