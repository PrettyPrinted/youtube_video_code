from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
    
class ItemDetail(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='details')
    detail = models.TextField()

    def __str__(self):
        return f"Detail for {self.item.name}"
