from django.db import models
from django.contrib.auth.models import User
# Create your models here.
GENDER_TYPE=(
  ('Male', 'Male'),
  ('Female', 'Female'),
)
class UserAccount(models.Model):
  user = models.OneToOneField(User, related_name="account", on_delete=models.CASCADE)
  gender = models.CharField(max_length=10,choices=GENDER_TYPE)
  phone_no = models.CharField(max_length=100)
  book_borrow_date = models.DateField(auto_now_add=True)
  balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)
  customer_id = models.IntegerField(unique=True)

  def __str__(self):
      return str (self.customer_id)