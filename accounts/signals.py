# importing predifined group model
from django.contrib.auth.models import Group

# import predefined User model
from django.contrib.auth.models import User

from .models import *

# import predefined User model
from django.contrib.auth.models import User

#importing post_save signal method
from django.db.models.signals import post_save


def create_customer(sender, instance, created, **kwargs):

	# if the a user is created => create a customer related to the user
	if created: 
		
		# get the group name
		group = Group.objects.get(name='customer')

		# add the user to the group
		instance.groups.add(group)

		#creating a customer object related to the new user
		Customer.objects.create(
			cust_user=instance,
			name=instance.username,
			email = instance.email,
		)

		print("Profile created")

# call create_customer() when a user is created
post_save.connect(create_customer, sender=User)