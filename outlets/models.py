from django.db import models
# from base.models import BaseModel

# Create your models here.



class Outlet(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
        
    def __str__(self) -> str:
        return self.name


class Comment(models.Model):
    outlet = models.ForeignKey(Outlet,on_delete=models.PROTECT)
    name = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    
    def __str__(self) -> str:
        return self.name