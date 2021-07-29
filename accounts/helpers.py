from django.contrib.auth.models import User


def check_duplicate_email(email_address) -> bool:
    try:
        if User.objects.filter(email=email_address).exists():
            return True
        return False
    except Exception as e:
        print("Exception in check_duplicate_email(accounts:helpers):", str(e))
        return False


def update_password(user_obj: User, pwd1: str, pwd2: str, prev_pass: str, check_prev_pass: bool = True) -> tuple:
    if pwd1 != pwd2:
        return False, "Passwords do not match"

    if check_prev_pass:
        if not user_obj.check_password(prev_pass):
            return False, "Old password incorrect"

    user_obj.set_password(pwd1)
    user_obj.save()
    return True, "Password updated successfully"
