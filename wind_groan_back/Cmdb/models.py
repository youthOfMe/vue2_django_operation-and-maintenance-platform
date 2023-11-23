from django.db import models
from mongoengine import (
    Document, DynamicDocument, EmbeddedDocument,
    StringField, IntField, BooleanField, ListField,
    EmbeddedDocumentField
)
# ODM

class CiTypeField(EmbeddedDocument):
    name = StringField(required=True, max_length=24)
    label = StringField(max_length=24)
    type = StringField(max_length=24) # 自定义的 可以是枚举
    required = BooleanField(default=False)



class CiType(Document):
    meta = { 'collection': 'citypes' } # 文档独立成立为一行时放在什么里面
    # id
    name = StringField(required=True, unique_with='version', max_length=24)
    version = IntField(required=True, default=1)
    label = StringField(max_length=24)
    fields = ListField(EmbeddedDocumentField(CiTypeField))

# 1. 空的Model类职位生成基本权限
# class CiType(models.Model):
#     pass


class Ci(DynamicDocument):
    """所有类型产生的所有实例"""
    meta = { 'collection': 'cis' }
    # 字段
