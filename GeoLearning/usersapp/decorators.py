from functools import wraps
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

def non_staff_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_staff:
            return redirect('home')
            return HttpResponseRedirect('/error')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
