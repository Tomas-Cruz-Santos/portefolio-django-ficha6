def user_groups(request):
    if request.user.is_authenticated:
        return {
            'is_gestor': request.user.groups.filter(name='gestor-portfolio').exists(),
            'is_autor': request.user.groups.filter(name='autores').exists(),
        }
    return {'is_gestor': False, 'is_autor': False}