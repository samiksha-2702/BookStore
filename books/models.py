from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='books/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books')
    created_at = models.DateTimeField(auto_now_add=True)
    is_bestseller = models.BooleanField(default=False)
    # new_arrival = models.BooleanField(default=False)
    # discount_percentage = models.IntegerField(default=0)
    # avg_rating = models.DecimalField(max_digits=2, decimal_places=1, default=4.0)
    # review_count = models.IntegerField(default=0)
    # is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    


