import datetime, time
from django.contrib.auth.models import User
from web.models import AttempLogin

# Minutos e intentos permitidos antes de bloquear
minutes_allowed = 3
attemps_allowed = 5


def check_username(username):
    user = None
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
    return user


def time_to_unlock(first_time):
    time_unlock = datetime.timedelta(hours=00, minutes=minutes_allowed, seconds=00)
    time = time_unlock + first_time.replace(tzinfo=None)
    return time


def is_blocked(username):
    block = False
    time_unblock = None
    if AttempLogin.objects.filter(user=username).exists():
        len_attemps = AttempLogin.objects.filter(user=username).count()
        if len_attemps > attemps_allowed-1:
            first_elem = len_attemps - attemps_allowed
            last_elem = len_attemps
            last_attemps_list = AttempLogin.objects.filter(user=username)[first_elem:last_elem]
            first_time = last_attemps_list[0].created_at
            last_time = last_attemps_list[4].created_at
            total_seconds = (last_time - first_time).total_seconds()
            time_allowed = minutes_allowed*60
            if total_seconds < time_allowed:
                block = True
                time_unblock = time_to_unlock(first_time)
    return block, time_unblock


def error_login_session(username):
    # Ha habido un error, aumentamos el contador
    # Comprobamos si existe el username
    auth_user = check_username(username)
    if auth_user:
        now = datetime.datetime.now()
        AttempLogin.objects.create(user=username, created_at=now)
        # Consultamos los intentos en los últimos 5 min
        block = is_blocked(username)
        return block,now


def clean_block_text(request):
    now = datetime.datetime.now().time()
    str_time_unlock = request.session.get('time_unblock')
    time_to_unlock_user = datetime.datetime.strptime(str_time_unlock, '%H:%M:%S').time()
    if now > time_to_unlock_user:
        request.session['message_login'] = None
        request.session['time_unblock'] = None