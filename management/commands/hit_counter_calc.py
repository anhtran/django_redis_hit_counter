from django.core.management.base import NoArgsCommand
import redis
from django.conf import settings
from redis_hit_counter.models import HitCount


REDIS_HOST = getattr(settings, 'REDIS_HOST', 'localhost')
REDIS_PORT = getattr(settings, 'REDIS_PORT', 6379)
REDIS_DB = getattr(settings, 'REDIS_DB', 0)


class Command(NoArgsCommand):
    help = "Calculate hits from redis and save them to MySQL."

    def handle_noargs(self, **options):
        r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

        for i in r.lrange('hit.count', 0, int(r.llen('hit.count')) - 1):
            try:
                h = HitCount.objects.get(pk=int(i))
                h.hits += 1
                h.save()
            except:
                pass
        r.flushdb()