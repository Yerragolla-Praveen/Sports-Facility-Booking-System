from django.db import models

class Customer(models.Model):
    first_name=models.CharField(max_length=20)
    last_name=models.CharField(max_length=20)
    mobile=models.IntegerField()
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=200)
    
    #checking if email is exist or not
    def isexist(self):
        if Customer.objects.filter(email=self.email):
            return True
        return False
    
    @staticmethod
    def getemail(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False