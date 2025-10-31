from clerk_backend_api import authenticate_request, AuthenticateRequestOptions, Clerk
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication

User = get_user_model()

class ClerkAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        if 'Authorization' not in request.headers:
            return None

        try:
            request_state = authenticate_request(
                request,
                AuthenticateRequestOptions(
                    secret_key=settings.CLERK_API_SECRET_KEY
                )
            )

            if not request_state.is_signed_in:
                print("Authentication failed!", request_state.message)
                return None

            with Clerk(bearer_auth=settings.CLERK_API_SECRET_KEY) as clerk:
                user_data = clerk.users.get(user_id=request_state.payload["sub"])
                primary_email_address_id = user_data.primary_email_address_id
                email = next(
                    (email for email in user_data.email_addresses if email.id == primary_email_address_id),
                    None
                )

            user, _ = User.objects.get_or_create(
                username=request_state.payload["sub"],
                defaults={"email": email.email_address}
            )

        except Exception as e:
            print(e)
            return None

        return (user, None)