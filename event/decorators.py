from django.contrib.auth.decorators import user_passes_test

def group_required(*group_names):
    """
    Allows access only to users who are in one of the given groups.
    """
    def in_groups(user):
        return user.is_authenticated and user.groups.filter(name__in=group_names).exists()
    return user_passes_test(in_groups)
