from django.urls import path
from .views import auth_view, verify_view, profile_view, referral_view, get_referrals_view

urlpatterns = [
    path('', auth_view, name='auth_view'),
    path('auth/<user_email>/<session_id>/', verify_view, name='verify_view'),
    path('profile/<user_email>/', profile_view, name='profile_view'),
    path('enter_referral/<user_email>/', referral_view, name='referral_view'),
    path('user_referrals/<user_email>/', get_referrals_view, name='get_referrals_view'),
]
