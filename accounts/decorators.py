from django.http import HttpResponse
from django.shortcuts import redirect

# decorator to check if a user is logged in or not
def check_authentication(view_function):
	def wrapper_function(request, *args, **kwargs):

		# if user is logged in -> this view is restricted 
		# redirect user to homepage
		if request.user.is_authenticated:
			return redirect('home')
		# return the requested view
		else :
			return view_function(request, *args, **kwargs)

	return wrapper_function

# to check different types of users 
def allowed_users(allowed_roles=[]):
	def decorator_func(view_func):
		def wrapper_func(request, *args, **kwargs):

			group = None

			# get the user's role
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name

			# if the user's role is allowed , return the requested view
			if group in allowed_roles:
				return view_func(request, *args, **kwargs)
			# show unauthorized error message
			else : 
				return HttpResponse('You are not authorized to access this page')

		return wrapper_func

	return decorator_func

# return different dashboard view for different users
def check_admin(view_func):
	def wrapper_func(request, *args, **kwargs):

		group = None

		# get the user's role
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name

		if group == 'customer':
			return redirect('user_page')
		
		if group == 'admin':
			return view_func(request, *args, **kwargs)

	return wrapper_func