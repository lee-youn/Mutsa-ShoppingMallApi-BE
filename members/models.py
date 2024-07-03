from django.db import models

class Member(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "member"

class Address(models.Model):
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=30)
    member = models.OneToOneField(Member, on_delete=models.CASCADE)

    class Meta:
        db_table = "address"