from tastypie.authentication import ApiKeyAuthentication

class ApiKeyAuthMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request's user is anonymous and if an API key is provided
        if request.user.is_anonymous and 'HTTP_AUTHORIZATION' in request.META:
            auth = ApiKeyAuthentication()
            user = auth.is_authenticated(request)

        response = self.get_response(request)
        return response
