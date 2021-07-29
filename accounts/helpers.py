from django.contrib.auth.models import User


def check_duplicate_email(email_address) -> bool:
    try:
        if User.objects.filter(email=email_address).exists():
            return True
        return False
    except Exception as e:
        print("Exception in check_duplicate_email(accounts:helpers):", str(e))
        return False
