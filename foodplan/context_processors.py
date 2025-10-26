from .models import User


def user_context(request):
    """Добавляет пользователя в контекст всех шаблонов"""
    user_data = None
    if 'user_id' in request.session:
        try:
            user = User.objects.get(id=request.session['user_id'])
            user_data = {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'phone': user.phone
            }
        except User.DoesNotExist:
            pass

    return {'current_user': user_data}