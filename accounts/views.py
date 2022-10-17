from django.shortcuts import render, redirect


from accounts.forms import SignUpForm

from home.views import homeview


# Create your views here.


def SignUpView(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(homeview)
    else:
        form = SignUpForm()

    return render(request, 'registration/signup.html', {'form': form})
