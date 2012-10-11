from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class HitCount(models.Model):
    """
    Model that stores the hit totals for any content object.

    """
    hits            = models.PositiveIntegerField(default=0)
    content_type    = models.ForeignKey(ContentType,
        verbose_name="content type",
        related_name="content_type_set_for_hit_counter",)
    object_pk       = models.TextField('object ID')
    content_object  = generic.GenericForeignKey('content_type', 'object_pk')

    class Meta:
        ordering = ( '-hits', )

    def __unicode__(self):
        return u'%s' % self.content_object


class BlacklistIP(models.Model):
    ip = models.CharField(max_length=40, unique=True)
    disable = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Blacklisted IP"
        verbose_name_plural = "Blacklisted IPs"

    def __unicode__(self):
        return u'%s' % self.ip


class BlacklistUserAgent(models.Model):
    user_agent = models.CharField(max_length=255, unique=True)
    disable = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Blacklisted User Agent"
        verbose_name_plural = "Blacklisted User Agents"

    def __unicode__(self):
        return u'%s' % self.user_agent
