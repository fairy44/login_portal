# from mainApp.models import TimeHistory
# def save_profile(backend, user, response, *args, **kwargs):    
#     if backend.name == 'google':  
#         new_object = TimeHistory(Username='Ayush')
#         new_object.save()
#         pass
        
from mainApp.models import TimeHistory  # Import your UserProfile model
from allauth.socialaccount.models import SocialAccount
# from allauth.socialaccount.models import SocialAccount,SocialLogin
from django.utils import timezone
from social_core.pipeline.user import user_details


def save_profile_with_google_id(strategy, backend, user, response, details, *args, **kwargs):
    if backend.name == 'google-oauth2':
        google_user_id = response.get('sub')  # 'sub' is the Google user ID

        # Check if the user exists
        if user is not None:
            # Check if the user already has a TimeHistory instance
            if hasattr(user, 'timehistory'):
                user.timehistory.google_id = google_user_id
                user.timehistory.save()
            else:
                # Create a new TimeHistory instance and associate it with the user
                TimeHistory.objects.create(user=user, google_id=google_user_id)
        else:
            user = User.objects.create(username=details.get('username'))
        # TimeHistory.objects.create(user=user, google_id=google_user_id)

            # Handle the case where the user doesn't exist (e.g., create a new user)
            pass  # Add your logic here

    # Continue with the default user_details pipeline step
    return user_details(strategy, backend, user, response, details, *args, **kwargs)