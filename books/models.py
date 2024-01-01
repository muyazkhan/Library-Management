from django.db import models
from django.contrib.auth.models import User
# Create your models here.
RATINGS = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5)
)

class category(models.Model):
    name = models.CharField("Name", max_length=100)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    def __str__(self):
        return self.name
    
class Book(models.Model):
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    book_name = models.CharField(max_length=25)
    book_description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='book_images/',blank=True,null=True)
    def __str__(self):
        return f"{self.book_name}"



class review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='review')
    user = models.ForeignKey(User, related_name="review", on_delete=models.CASCADE)
    body = models.TextField()
    ratings = models.IntegerField(choices=RATINGS)
    timestamps = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return f"Review by {self.user.username}"

# Create your models here.
class BorrowBook(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)

    def __str__(self):
        return f"borrow this Book : {self.book.Name}"