from django.db import models
from menu.models import FoodItem
from accounts.models import User


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_carts',
        verbose_name='User',
    )
    fooditem = models.ForeignKey(
        FoodItem,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Food Item',
    )
    quantity = models.PositiveIntegerField(default=1,verbose_name='Quantity')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        ordering = ('fooditem',)
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

    def __str__(self):
        return self.user.email


