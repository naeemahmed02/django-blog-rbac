
def logged_in_dec(func):
    def login_req():
        if request.user.is_authenticated:
            return redirect(request.path)
        else:
            return redirect('user_login')
    return login_req()