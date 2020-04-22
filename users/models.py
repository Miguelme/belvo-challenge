import uuid

from django.db import models


class User(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=128)
	email = models.EmailField()
	age = models.IntegerField()

	def __str__(self):
		return self.id + ":" + self.name


class Transaction(models.Model):
	user = models.ForeignKey(User, related_name='transactions', on_delete=models.CASCADE)
	reference = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4, primary_key=True)
	account = models.CharField(max_length=128)
	date = models.DateField()
	amount = models.DecimalField(max_digits=16, decimal_places=2)
	type = models.CharField(max_length=10, choices=(('inflow', 'inflow'), ('outflow', 'outflow')))
	category = models.CharField(max_length=128)

	def __str__(self):
		return self.reference