from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm

# Create your views here.

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

def products(request):

	products = Product.objects.all()

	param = { 'product_list' : products }

	return render(request, 'accounts/products.html', param)

def customers(request, cust_id):

	customer = Customer.objects.get(id = cust_id)

	orders = customer.order_set.all()
	order_count = orders.count()

	print(order_count)	

	context = { 'cust' : customer,
				'cust_orders' : orders,
				'totalOrders' : order_count, 
	 }

	return render(request, 'accounts/customers.html', context)

def createOrder(request):

	form = OrderForm()
	if request.method == 'POST':
		form = OrderForm(request.POST)
		if form.is_valid():
			form.save()
		return redirect('/')	


	context = {'orderform' : form}
	return render(request, 'accounts/order_form.html', context)


def updateOrder(request, pk):
	order =  Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
		return redirect('/')

	context = {'orderform' : form}
	return render(request, 'accounts/order_form.html', context)

def deleteOrder(request, pk):
	order =  Order.objects.get(id=pk)

	if request.method == 'POST':
		order.delete()
		return redirect('/')

	context = {'item' : order}
	return render(request, 'accounts/delete.html', context)

