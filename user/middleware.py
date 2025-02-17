from django.utils import timezone
from .forms import ProfileForm
import json
from django.forms.utils import ErrorDict, ErrorList
from django.conf import settings
from django.shortcuts import redirect

class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if not hasattr(request.user, 'profile'):
                request.show_profile_modal = True

                # Check if we have stored form errors
                if 'profile_form_errors' in request.session:

                    # Recreate form with previous data
                    form_data = request.session.get('profile_form_data', {})
                    request.profile_form = ProfileForm(form_data)

                    # Load and apply errors
                    errors_json = json.loads(request.session['profile_form_errors'])
                    error_dict = ErrorDict()

                    for field, field_errors in errors_json.items():
                        error_list = ErrorList()
                        for error in field_errors:
                            if isinstance(error, dict) and 'message' in error:
                                error_list.append(error['message'])
                            else:
                                error_list.append(error)
                        error_dict[field] = error_list

                    request.profile_form._errors = error_dict

                    # Clear stored errors and data
                    del request.session['profile_form_errors']
                    if 'profile_form_data' in request.session:
                        del request.session['profile_form_data']
                else:
                    # Only initialize a fresh form on GET requests
                    if request.method == 'GET':
                        request.profile_form = ProfileForm()
            else:
                request.show_profile_modal = False
                request.profile_form = None

        response = self.get_response(request)
        return response

class UpdateLastSeenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            request.user.last_seen=timezone.now()
            request.user.save(update_fields=['last_seen'])
        return response