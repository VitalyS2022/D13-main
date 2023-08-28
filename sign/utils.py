
from django.contrib.auth import authenticate, login


def usual_login_view(request):
    username = request.POST['username']
    # password = request.POST['password']
    # user = authenticate(request, username=username, password=password)
    print('**************', request.POST)
    print('******', username)

    # if user is not None:
    #     print('***', '111')
    #     # OneTimeCode.objects.create(code=random.choice('1234567890'), user=user)
    #     # send_mail()
    #     # redirect html
    # else:
    #     pass

# def login_with_code_view(request):
#     username = request.POST['username']
#     code = request.POST['code']
#     if OneTimeCode.objects.filter(code=code, user__username=username).exists():
#         login(request, user)
#     else:
#         # error
