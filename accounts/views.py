from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm, SignupForm
from .filters import *

from django.contrib.auth.forms import UserCreationForm

# importing predifined group model
from django.contrib.auth.models import Group

# used for creating multiple forms within one form
from django.forms import inlineformset_factory 

# This line is used for importing flash messages
from django.contrib import messages

# This import helps to auttheticate, login, logout
from django.contrib.auth import authenticate, login, logout

# This import is used to restrict user access
from django.contrib.auth.decorators import login_required

# importing decorators 
from .decorators import *

# Create your views here.


# This decorator restricts the view for unauthenticated users
@login_required(login_url='login')
# this decorator restricts the dashboard based on user's role
@check_admin
def home(request):

	orders = Order.objects.all()
	customers = Customer.objects.all()

	total_customers = customers.count()
	total_orders = orders.count()

	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	context = {
		'cust_list' : customers,
		'order_list' : orders,
		'cust_count' : total_customers,
		'order_count' : total_orders,
		'delivered_count' : delivered,
		'pending_count' : pending,

	}


	return render(request, 'accounts/dashboard.html', context)


@check_authentication
def loginPage(request):

	if request.method == 'POST':
		user_name = request.POST.get('username')
		pass_word = request.POST.get('password')

		user = authenticate(request, username=user_name, password=pass_word)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username Or Password is incorrect')

	return render(request, 'accounts/login.html')

@check_authentication
def signupPage(request):
	
	form = SignupForm()

	if request.method == "POST":
		form = SignupForm(request.POST)
		if form.is_valid():
			
			user = form.save()

			# get the group name
			group = Group.objects.get(name='customer')

			# add the user to the group
			user.groups.add(group)

			messages.success(request, 'Account Created Successfully')
			return redirect('login')

	context = {
		'signupform' : form,
	}

	return render(request, 'accounts/signup.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')


def userPage(request):
	context = {}
	return render(request, 'accounts/user.html', context)

# This line restricts the view for unauthenticated users
@login_required(login_url='login')
# this decorator restricts the view based on user's role
@allowed_users(allowed_roles=['admin'])
def products(request):

	products = Product.objects.all()

	param = { 'product_list' : products }

	return render(request, 'accounts/products.html', param)


# This line restricts the view for unauthenticated users
@login_required(login_url='login')
# this decorator restricts the view based on user's role
@allowed_users(allowed_roles=['admin'])
def customers(request, cust_id):

	customer = Customer.objects.get(id = cust_id)

	orders = customer.order_set.all()
	order_count = orders.count()

	orderFilterForm = OrderFilter(request.GET, queryset=orders)
	orders = orderFilterForm.qs	

	context = { 'cust' : customer,
				'cust_orders' : orders,
				'totalOrders' : order_count,
				'orderFilterForm' : orderFilterForm, 
	 }

	return render(request, 'accounts/customers.html', context)


# This line restricts the view for unauthenticated users
@login_required(login_url='login')
# this decorator restricts the view based on user's role
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
	# gets the customer with the given primary key
	customer = Customer.objects.get(id=pk)
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
	formset = OrderFormSet(queryset = Order.objects.none(), instance=customer)

	if request.method == 'POST':
		try:
			formset = OrderFormSet(request.POST, instance=customer)
		except ValidationError :
			formset = None

		if formset.is_valid():
			formset.save()
		return redirect('/')	


	context = {'orderformset' : formset}
	
	return render(request, 'accounts/order_form.html', context)


# This line restricts the view for unauthenticated users
@login_required(login_url='login')
# this decorator restricts the view based on user's role
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
	order =  Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
		return redirect('/')


	context = {'orderformset' : form}
	
	return render(request, 'accounts/order_form.html', context)


# This line restricts the view for unauthenticated users
@login_required(login_url='login')
# this decorator restricts the view based on user's role
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
	order =  Order.objects.get(id=pk)

	if request.method == 'POST':
		order.delete()
		return redirect('/')

	context = {'item' : order}
	return render(request, 'accounts/delete.html', context)



