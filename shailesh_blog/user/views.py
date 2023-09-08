from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

#sign_up using function based view
def sign_up(request):
    html = "user/signup.html"
    print(dir(request),"first") #<WSGIRequest: GET '/user/sign-up/'>
    # print(request.COOKIES,"COOKIES")
    print(request.get_full_path,"--------")
    res = "<h1>Hello ,Welcome to Sign Up page</h1>"
    # return HttpResponse(res)
    return render(request,html,{"1":"One"})
