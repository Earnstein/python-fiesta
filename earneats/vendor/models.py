from django.db import models
from django.db.models import QuerySet
from django.utils import timezone
from datetime import time
from accounts.models import User , UserProfile
from accounts.utils import send_vendor_approval_email
from django.db.models import Case, When, Value, BooleanField, Q, Exists, OuterRef, Prefetch

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
        """Base queryset for approved vendors only."""
        return super().get_queryset().filter(is_approved=True, user__is_active=True)
    
    def _get_current_datetime_info(self):
        """Get current datetime info, can be cached if needed."""
        now = timezone.now()
        return {
            'current_day': now.isoweekday(),
            'current_time': now.time(),
            'now': now
        }
    
    def with_opening_status(self):
        """Get approved vendors with their current opening status annotated."""
        dt_info = self._get_current_datetime_info()
        
        # Create a subquery to check if vendor has opening hours for today
        today_opening_hours = OpeningHours.objects.filter(
            vendor=OuterRef('pk'),
            day_of_week=dt_info['current_day'],
            is_open=True,
            from_hour__lte=dt_info['current_time'],
            to_hour__gte=dt_info['current_time'],
            from_hour__isnull=False,
            to_hour__isnull=False,
        )
        
        return self.get_queryset().annotate(
            is_currently_open=Exists(today_opening_hours)
        ).select_related('user', 'user_profile')
    
    def currently_open(self):
        """Get only approved vendors that are currently open."""
        dt_info = self._get_current_datetime_info()
        
        return self.get_queryset().filter(
            opening_hours__day_of_week=dt_info['current_day'],
            opening_hours__is_open=True,
            opening_hours__from_hour__lte=dt_info['current_time'],
            opening_hours__to_hour__gte=dt_info['current_time'],
            opening_hours__from_hour__isnull=False,
            opening_hours__to_hour__isnull=False,
        ).select_related('user', 'user_profile').distinct()
    
    def currently_closed(self):
        """Get only approved vendors that are currently closed."""
        dt_info = self._get_current_datetime_info()
        
        # Get vendors that are either not open today or outside business hours
        return self.get_queryset().exclude(
            Q(opening_hours__day_of_week=dt_info['current_day']) &
            Q(opening_hours__is_open=True) &
            Q(opening_hours__from_hour__lte=dt_info['current_time']) &
            Q(opening_hours__to_hour__gte=dt_info['current_time']) &
            Q(opening_hours__from_hour__isnull=False) &
            Q(opening_hours__to_hour__isnull=False)
        ).select_related('user', 'user_profile').distinct()
    
    def with_todays_hours(self):
        """Get approved vendors with today's opening hours prefetched."""
        dt_info = self._get_current_datetime_info()
        
        return self.get_queryset().prefetch_related(
            Prefetch(
                'opening_hours',
                queryset=OpeningHours.objects.filter(day_of_week=dt_info['current_day']),
                to_attr='todays_hours'
            )
        ).select_related('user', 'user_profile')
    
    def with_complete_opening_status(self):
        """Get approved vendors with opening status and today's hours."""
        dt_info = self._get_current_datetime_info()
        
        # Create a subquery to check if vendor has opening hours for today
        today_opening_hours = OpeningHours.objects.filter(
            vendor=OuterRef('pk'),
            day_of_week=dt_info['current_day'],
            is_open=True,
            from_hour__lte=dt_info['current_time'],
            to_hour__gte=dt_info['current_time'],
            from_hour__isnull=False,
            to_hour__isnull=False,
        )
        
        return self.get_queryset().prefetch_related(
            Prefetch(
                'opening_hours',
                queryset=OpeningHours.objects.filter(day_of_week=dt_info['current_day']),
                to_attr='todays_hours'
            )
        ).annotate(
            is_currently_open=Exists(today_opening_hours)
        ).select_related('user', 'user_profile')
    
    def open_at_time(self, check_time, day_of_week=None):
        """Get approved vendors that are open at a specific time."""
        if day_of_week is None:
            day_of_week = timezone.now().isoweekday()
        
        return self.get_queryset().filter(
            opening_hours__day_of_week=day_of_week,
            opening_hours__is_open=True,
            opening_hours__from_hour__lte=check_time,
            opening_hours__to_hour__gte=check_time,
            opening_hours__from_hour__isnull=False,
            opening_hours__to_hour__isnull=False,
        ).select_related('user', 'user_profile').distinct()
    
    def with_all_hours(self):
        """Get approved vendors with all opening hours prefetched."""
        return self.get_queryset().prefetch_related(
            'opening_hours'
        ).select_related('user', 'user_profile')
    
    def using_subquery_approach(self):
        """Alternative approach using Exists subquery for opening status."""
        dt_info = self._get_current_datetime_info()
        
        currently_open_subquery = OpeningHours.objects.filter(
            vendor=OuterRef('pk'),
            day_of_week=dt_info['current_day'],
            is_open=True,
            from_hour__lte=dt_info['current_time'],
            to_hour__gte=dt_info['current_time'],
            from_hour__isnull=False,
            to_hour__isnull=False,
        )
        
        return self.get_queryset().annotate(
            is_currently_open=Exists(currently_open_subquery)
        ).select_related('user', 'user_profile')
    
    def for_listing_page(self):
        """Optimized query for vendor listing pages."""
        return self.with_complete_opening_status().only(
            'id', 'vendor_name', 'vendor_slug', 'vendor_license',
            'user__email', 'user_profile__profile_picture'
        )
    
    def with_opening_status_and_distance(self, point):
        """Get approved vendors with opening status and distance annotation."""
        from django.contrib.gis.db.models.functions import Distance
        
        dt_info = self._get_current_datetime_info()
        
        # Create a subquery to check if vendor has opening hours for today
        today_opening_hours = OpeningHours.objects.filter(
            vendor=OuterRef('pk'),
            day_of_week=dt_info['current_day'],
            is_open=True,
            from_hour__lte=dt_info['current_time'],
            to_hour__gte=dt_info['current_time'],
            from_hour__isnull=False,
            to_hour__isnull=False,
        )
        
        return self.get_queryset().annotate(
            is_currently_open=Exists(today_opening_hours),
            distance=Distance("user_profile__location", point)
        ).select_related('user', 'user_profile')

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

    class Meta:
        verbose_name = 'vendor'
        verbose_name_plural = 'vendors'
        indexes = [
            models.Index(fields=['vendor_name'], name='vendor_name_idx'),
        ]

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
        unique_together = (('vendor', 'day_of_week'),)
        ordering = ['day_of_week']

        
        # indexes for better query performance
        indexes = [
            models.Index(fields=['day_of_week', 'vendor']),
            models.Index(fields=['day_of_week', 'is_open', 'from_hour', 'to_hour']),
            models.Index(fields=['vendor', 'day_of_week', 'is_open']),
        ]

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