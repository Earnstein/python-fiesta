from django.db import models
from django.db.models import QuerySet
from accounts.models import User , UserProfile
from accounts.utils import send_vendor_approval_email


class ApprovedManager(models.Manager):
    def get_queryset(self) -> QuerySet['Vendor']:
        return super().get_queryset().filter(is_approved=True, user__is_active=True)


class Vendor(models.Model):
    user = models.OneToOneField(User, related_name="user", on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name="userprofile", on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
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
                if self.is_approved == True:
                    # SEND APPROVAL EMAIL
                    mail_subject = "Congratulations! Your resturant has been approved"
                else:
                    # SEND REJECTION EMAIL
                    mail_subject = "We're sorry ! You are not eligible for publishing your food menu on Earneats"
                send_vendor_approval_email(mail_subject, mail_template, context)
        return super(Vendor, self).save(*args, **kwargs)

    def __str__(self):
        return self.vendor_name 