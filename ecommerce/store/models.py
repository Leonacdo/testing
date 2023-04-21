from django.db import models
from django.contrib.auth.models import User #add this
from django.dispatch import receiver #add this
from django.db.models.signals import post_save #add this 

CATEGORY = [
    ("T", "Tv"),
    ("S", "SmartPhone"),
    ("C", "Clothes"),
    ("P", "Pets"),
    ("O", "Other"),
]



# Create your models here.
class Product(models.Model):
  name=models.CharField(max_length=150)
  product_type=models.CharField(max_length=150)
  description=models.TextField()
  category = models.CharField(max_length=300, choices = CATEGORY) 

  price=models.FloatField()
  image=models.ImageField(upload_to='image/')
  
  def __str__(self):
    return self.name
    
class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  products = models.ManyToManyField(Product)
  
  def __str__(self):
    return f'{self.user} profile'
  
  @receiver(post_save, sender=User) #add this
  def create_user_profile(sender, instance, created, **kwargs):
    if created:
      Profile.objects.create(user=instance)
      
  @receiver(post_save, sender=User) #add this
  def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Vote(models.Model):   #add this class and the following fields
	profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	comfort = models.IntegerField(default=0)
	performance = models.IntegerField(default=0)
	durability = models.IntegerField(default=0)
