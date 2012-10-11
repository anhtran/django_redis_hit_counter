from django.conf.urls import patterns, url

urlpatterns = patterns('redis_hit_counter.views',
    url(r'^ajax/update/hit_count/$', 'update_hit_count', name='update_hit_count'),
)