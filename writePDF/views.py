from django.http import HttpResponse
from django.shortcuts import render, redirect
from chrisproject import produce_pdf, client_list, peerGrp_list


# Create your views here.
def home_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        userName = request.user
        con = {
            "user_name": userName,
            "c_list": client_list(),
            "p_list": peerGrp_list()
        }
        if request.method == "POST":
            client_index = request.POST.get('client_id')
            peerGrp_index = request.POST.get('peerGrp_id')
            produce_pdf(int(client_index), int(peerGrp_index))
        return render(request, "home.html", con)
    else:
        print("Log in required.")
        return redirect("/login")