from django.shortcuts import render
from api.forms import reset_form
from api.models import User
from django.http import HttpResponseRedirect


def change_password(request):

    if request.method == 'POST':
        form = reset_form(request.POST)
        if form.is_valid():
            newpassword=form.cleaned_data['newpassword']
            user = User.objects.get(email=request.user.email)
            if user is not None:
                user.set_password(str(newpassword))
                user.save()
                return HttpResponseRedirect('/login/')
            else:
                return render(request, 'password.html',{'error':'You have entered wrong old password','form': form})

        else:
           return render(request, 'password.html',{'error':'You have entered old password','form': form})
    else:
        form = reset_form()
    return render(request, 'password.html', {'form': form})