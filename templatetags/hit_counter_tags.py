from django import template
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from redis_hit_counter.models import HitCount


register = template.Library()


@register.simple_tag()
def hit_counter_js(obj):
    ctype = ContentType.objects.get_for_model(obj.__class__)
    hit_obj, created = HitCount.objects.get_or_create(content_type=ctype, object_pk=obj.pk)

    return """$.post('%(url)s', { hit_counter_pk: %(pk)s }, function(data) {if (data.status=='error') { console.log('Cannot update view count.'); }}, 'json');
    """ % {'url': reverse('update_hit_count'), 'pk': hit_obj.pk}


@register.assignment_tag()
def hit_counter(obj):
    ctype = ContentType.objects.get_for_model(obj.__class__)
    hit_obj, created = HitCount.objects.get_or_create(content_type=ctype, object_pk=obj.pk)
    if int(hit_obj.hits) > 0:
        return str(hit_obj.hits)
    else:
        return 0