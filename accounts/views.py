from django.shortcuts import render
from django.http import HttpResponse
from .models import *

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


