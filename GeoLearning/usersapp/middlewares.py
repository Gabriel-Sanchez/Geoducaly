from django.shortcuts import redirect
from django.urls import reverse

class ProfileComplitionMiddleware:

    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_anonymous:
            estudiante = request.user.estudiante
            if not estudiante.picture:
                if request.path not in [reverse('update_profile'), reverse('logout')]:
                    return redirect('update_profile')
        response = self.get_response(request)
        return response 
