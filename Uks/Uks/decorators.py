from django.http import HttpResponse
from django.shortcuts import redirect


def authorized(roles=[]):                                                   #Custom authorization 
        def decorator(view_func):
            def wrapper_func(request, *args, **kwargs):
                groups = []
                is_authorized = False

                if request.user.groups.exists():                            #Check ih user is in right group
                    for group in request.user.groups.all():                 #Store user gropus in list
                        groups.append(group.name);
                    
                    
                    groups_set = set(groups)                                
                    roles_set = set(roles)

                    if(groups_set & roles_set):                             #Comapre user groups and auth roles
                        is_authorized = True

                if(is_authorized):
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponse("Authorization failed!")
                    
            return wrapper_func
        return decorator
