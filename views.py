from django.http import HttpResponse
from django.utils.encoding import force_unicode
from django.views.decorators.csrf import csrf_protect
import simplejson as json
import redis
from django.conf import settings
from redis_hit_counter.utils import get_ip
import time
from redis_hit_counter.models import BlacklistIP, BlacklistUserAgent


REDIS_HOST = getattr(settings, 'REDIS_HOST', 'localhost')
REDIS_PORT = getattr(settings, 'REDIS_PORT', 6379)
REDIS_DB = getattr(settings, 'REDIS_DB', 0)
HIT_COUNTER_PERIOD = getattr(settings, 'HIT_COUNTER_PERIOD', 60*30)


@csrf_protect
def update_hit_count(request):
    result = ''
    error = ''
    if request.is_ajax():
        hit_counter_pk = request.POST.get('hit_counter_pk', None)
        if hit_counter_pk is not None:
            try:
                r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

                # check IP and user agent
                ip = get_ip(request)
                user_agent = request.META.get('HTTP_USER_AGENT', '')[:255]
                blacklist_ip = BlacklistIP.objects.filter(disable=False)
                blacklist_ua = BlacklistUserAgent.objects.filter(disable=False)
                if str(ip) not in blacklist_ip and user_agent not in blacklist_ua:
                    if not r.get('hit:%s:ip' % int(hit_counter_pk)) and not r.get('hit:%s:user.agent' % int(hit_counter_pk)):
                        r.rpush('hit.count', hit_counter_pk)
                        r.set('hit:%s:ip' % int(hit_counter_pk), ip)
                        r.set('hit:%s:user.agent' % int(hit_counter_pk), user_agent)
                        r.set('hit:%s:time' % int(hit_counter_pk), int(time.time()))
                        result = 'OK'
                    else:
                        if str(r.get('hit:%s:ip' % int(hit_counter_pk))) == str(ip):
                            if int(time.time()) - int(r.get('hit:%s:time' % int(hit_counter_pk))) >= HIT_COUNTER_PERIOD or \
                                r.get('hit:%s:user.agent' % int(hit_counter_pk)) != user_agent:
                                r.rpush('hit.count', hit_counter_pk)
                                r.set('hit:%s:ip' % int(hit_counter_pk), ip)
                                r.set('hit:%s:user.agent' % int(hit_counter_pk), user_agent)
                                r.set('hit:%s:time' % int(hit_counter_pk), int(time.time()))
                                result = 'OK'
                        else:
                            r.rpush('hit.count', hit_counter_pk)
                            r.set('hit:%s:ip' % int(hit_counter_pk), ip)
                            r.set('hit:%s:user.agent' % int(hit_counter_pk), user_agent)
                            r.set('hit:%s:time' % int(hit_counter_pk), int(time.time()))
                            result = 'OK'

            except Exception as e:
                error = e
        else:
            error = 'Cannot get the place id'
    else:
        error = 'AJAX required!'

    content = json.dumps({'result':force_unicode(result), 'error': force_unicode(error)})
    return HttpResponse(content, content_type='application/json')
