from django.db import models
from django.db.models import QuerySet
from django.utils import timezone
from datetime import time
from accounts.models import User , UserProfile
from accounts.utils import send_vendor_approval_email


DAY_OF_WEEK_CHOICES = [
    (1, 'Monday'),
    (2, 'Tuesday'),
    (3, 'Wednesday'),
    (4, 'Thursday'),
    (5, 'Friday'),
    (6, 'Saturday'),
    (7, 'Sunday')
]


class ApprovedManager(models.Manager):
    def get_queryset(self) -> QuerySet['Vendor']:
        return super().get_queryset().filter(is_approved=True, user__is_active=True)


class Vendor(models.Model):
    user = models.OneToOneField(User, related_name="user", on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name="userprofile", on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    vendor_slug = models.SlugField(max_length=100, unique=True)
    vendor_license = models.ImageField(upload_to="vendor/license")
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    approved = ApprovedManager()

    def save(self, *args, **kwargs):
        # UPDATE
        if self.pk is not None:
            orig = Vendor.objects.get(pk = self.pk)
            if orig.is_approved != self.is_approved:
                mail_template = "accounts/emails/admin_approval_email_template.html"
                context = {
                        "user": self.user,
                        "is_approved": self.is_approved
                    }
                if self.is_approved:
                    # SEND APPROVAL EMAIL
                    mail_subject = "Congratulations! Your resturant has been approved"
                else:
                    # SEND REJECTION EMAIL
                    mail_subject = "We're sorry ! You are not eligible for publishing your food menu on Earneats"
                send_vendor_approval_email(mail_subject, mail_template, context)
        return super(Vendor, self).save(*args, **kwargs)

    def __str__(self):
        return self.vendor_name 

    def get_opening_hours_for_day(self, day_of_week):
        """Get opening hours for a specific day."""
        try:
            return self.opening_hours.get(day_of_week=day_of_week)
        except OpeningHours.DoesNotExist:
            return None

    def is_currently_open(self):
        """Check if the vendor is currently open."""
        now = timezone.now()
        current_day = now.isoweekday()
        
        opening_hours = self.get_opening_hours_for_day(current_day)
        if not opening_hours:
            return False
            
        return opening_hours.is_currently_open()

    def get_all_opening_hours(self):
        """Get all opening hours ordered by day."""
        return self.opening_hours.all().order_by('day_of_week')



class OpeningHours(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="opening_hours")
    day_of_week = models.IntegerField(choices=DAY_OF_WEEK_CHOICES)
    from_hour = models.TimeField(blank=True, null=True)
    to_hour = models.TimeField(blank=True, null=True)
    is_open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'opening hours'
        verbose_name_plural = 'opening hours'
        unique_together = (('vendor', 'day_of_week'),
            ('day_of_week', 'from_hour', 'to_hour'))
        ordering = ['day_of_week']

    def __str__(self):
        day_name = dict(DAY_OF_WEEK_CHOICES)[self.day_of_week]
        if self.is_open and self.from_hour and self.to_hour:
            return f"{day_name} - {self.from_hour.strftime('%I:%M %p')} to {self.to_hour.strftime('%I:%M %p')}"
        return f"{day_name} - Closed"

    def get_day_name(self):
        """Get the day name from the choice."""
        return dict(DAY_OF_WEEK_CHOICES)[self.day_of_week]

    def get_formatted_hours(self):
        """Get formatted opening hours as string."""
        if not self.is_open or not self.from_hour or not self.to_hour:
            return "Closed"
        return f"{self.from_hour.strftime('%I:%M %p')} - {self.to_hour.strftime('%I:%M %p')}"

    def is_currently_open(self):
        """Check if the vendor is currently open on this day and time."""
        if not self.is_open or not self.from_hour or not self.to_hour:
            return False
        
        now = timezone.now()
        current_time = now.time()
        current_day = now.isoweekday()  # Monday=1, Sunday=7
        
        # Check if it's the right day
        if current_day != self.day_of_week:
            return False
        
        # Check if current time is within opening hours
        return self.from_hour <= current_time <= self.to_hour

    def clean(self):
        """Validate that from_hour is before to_hour."""
        from django.core.exceptions import ValidationError
        
        if self.is_open and self.from_hour and self.to_hour and self.from_hour >= self.to_hour:
            raise ValidationError("Opening time must be before closing time.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)