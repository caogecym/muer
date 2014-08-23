from rest_framework import permissions


class PostViewPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        '''
        Handles list level url permissions
        '''
        # unlogged in users can only GET
        if request.user and not request.user.is_authenticated():
            return request.method == 'GET'
        # logged in users can GET and POST
        else:
            return True

    def has_object_permission(self, request, view, obj):
        '''
        Handles object level url permissions
        '''
        # any user can GET a detail of a post
        if request.method in ['GET']:
            return True
        # staff have all permissions
        elif request.user and request.user.is_staff:
            return True
        # only logged in user can self PUT, DELETE
        else:
            return request.user == obj.author


class TagViewPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        '''
        Handles list level url permissions
        '''
        # unlogged in users can only GET
        if request.user and not request.user.is_authenticated():
            return request.method == 'GET'
        # logged in users can GET and POST
        else:
            return True

    def has_object_permission(self, request, view, obj):
        '''
        Handles object level url permissions
        '''
        # any user can GET a detail of a tag
        if request.method in ['GET']:
            return True
        # staff have all permissions
        elif request.user and request.user.is_staff:
            return True
        # only logged in user can POST
        elif request.user.is_authenticated():
            return request.method == 'POST'
        else:
            return False


class CommentViewPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        '''
        Handles list level url permissions
        '''
        # unlogged in users can only GET
        if request.user and not request.user.is_authenticated():
            return request.method == 'GET'
        # logged in users can GET and POST
        else:
            return True

    def has_object_permission(self, request, view, obj):
        '''
        Handles object level url permissions
        '''
        # any user can GET a detail of a post
        if request.method in ['GET']:
            return True
        # staff have all permissions
        elif request.user and request.user.is_staff:
            return True
        # only logged in user can self PUT, DELETE
        else:
            return request.user == obj.author


class UserViewPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        '''
        Handles list level url permissions
        '''
        # non staff users can only GET
        if request.user and not request.user.is_staff:
            return request.method == 'GET'
        else:
            return True

    def has_object_permission(self, request, view, obj):
        '''
        Handles object level url permissions
        '''
        # any user can GET a detail of a User
        if request.method in ['GET']:
            return True
        # staff have all permissions
        elif request.user and request.user.is_staff:
            return True
        # nothing else
        else:
            return False
