from django.contrib.auth.decorators import user_passes_test

def group_required(*group_names):
    """
    Allows access only to users who are in one of the given groups.
    Usage:
        @login_required
        @group_required('Admin', 'Organizer')
        def my_view(request):
            ...
    """
    def in_groups(user):
        return user.is_authenticated and user.groups.filter(name__in=group_names).exists()
    return user_passes_test(in_groups)



def admin_only(view_func):
    """
    Allows access only to users in Admin group or superusers.
    """
    def check(user):
        return user.is_authenticated and (user.is_superuser or user.groups.filter(name='Admin').exists())
    return user_passes_test(check)(view_func)


def organizer_only(view_func):
    """
    Allows access only to users in Organizer group.
    """
    decorator = user_passes_test(lambda u: u.is_authenticated and u.groups.filter(name='Organizer').exists())
    return decorator(view_func)

def participant_only(view_func):
    """
    Allows access only to users in Participant group.
    """
    decorator = user_passes_test(lambda u: u.is_authenticated and u.groups.filter(name='Participant').exists())
    return decorator(view_func)
