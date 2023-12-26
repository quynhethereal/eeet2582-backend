from django.db import models
from .user_model import User

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment')
    stripe_subscription_id = models.CharField(max_length=255, unique=True)
    stripe_customer_id = models.CharField(max_length=255, unique=True)
    plan_name =models.CharField(max_length=255)
    status = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    price = models.FloatField()

    
    def __str__(self):
        return f"{self.user.email} "
    
    def save(self, *args, **kwargs):
        # Set plan_name based on the status
        if self.status.lower() == 'trialing':
            self.plan_name = "20-days trial"
            self.price = 0
        elif self.status.lower() == 'active' and self.plan_name.lower() == '3m':
            self.plan_name = "3 Months"
        elif self.status.lower() == 'active' and self.plan_name.lower == '6m':
            self.plan_name = "6 Months"
        elif self.status.lower() == 'active' and self.plan_name.lower == '1y':
            self.plan_name = "12 Months"
        else:
            self.plan_name = "inactive"


        super().save(*args, **kwargs)
