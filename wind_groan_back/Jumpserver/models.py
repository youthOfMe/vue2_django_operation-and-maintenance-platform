from django.db import models

# Create your models here.
class Organization(models.Model):
    class Meta:
        db_table = 'js_org'

    # id
    name = models.CharField(max_length=24)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, null=True, verbose_name='父级ID')
    is_deleted = models.BooleanField(default=False) # 逻辑删除

    def __str__(self):
        return "<Org {}, {} -> {}>".format(self.pk, self.name, self.parent_id)