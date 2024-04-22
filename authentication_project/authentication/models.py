from django.db import models


class UserProfile(models.Model):
    email = models.CharField(max_length=50, unique=True)
    referral_code = models.CharField(max_length=6, blank=True, null=True)
    referred_emails = models.ManyToManyField('self', symmetrical=False, related_name='referrals', blank=True)
    activated_invite_code = models.BooleanField(default=False)

    def __str__(self):
        return self.email
