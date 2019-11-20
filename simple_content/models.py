from django.db import models
from mptt.models import TreeForeignKey, MPTTModel
from pytils.translit import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Content(MPTTModel):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(blank=True, null=False)
    parent = TreeForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children')
    content = models.TextField(null=True, blank=True)
    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True)

    node_order_by = ['title']

    def __str__(self):
        return self.title

    @property
    def get_absolute_url(self):
        parent = self.parent  # type: Content
        if parent is not None:
            url = '{parent_absolute_url}{slug}/'.format(
                parent_absolute_url=parent.get_absolute_url,
                slug=self.slug
            )
        else:
            url = '/{slug}/'.format(slug=self.slug)
        return url

    class Meta:
        ordering = ()

@receiver(pre_save, sender=Content)
def content_pre_save(sender, instance, **kwargs):
    if not instance.slug and instance._state.adding:
            instance.slug = slugify(instance.title)
