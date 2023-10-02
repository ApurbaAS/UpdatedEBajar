from django.shortcuts import redirect

def simple_middleware(get_response):
    
    
    def middleware(request):
        return_url = request.META['PATH_INFO']
        if not request.session.get('user_id'):
            return redirect(f'login?return_url={return_url}')
            
        
        response = get_response(request)
        
        return response

    return middleware