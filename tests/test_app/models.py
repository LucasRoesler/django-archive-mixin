from django.db import models

from django_archive_mixin.mixins import ArchiveMixin


class BaseModel(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)


class NullRelatedModel(models.Model):
    nullable_base = models.ForeignKey(BaseModel, blank=True, null=True)


class BaseArchiveModel(ArchiveMixin, models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)


class RelatedModel(models.Model):
    base = models.ForeignKey(BaseArchiveModel)
    null_base = models.ForeignKey(BaseArchiveModel, blank=True, null=True)
    set_null_base = models.ForeignKey(
        BaseArchiveModel,
        blank=True, null=True, on_delete=models.deletion.SET_NULL)
    set_default_base = models.ForeignKey(
        BaseArchiveModel,
        blank=True, null=True, on_delete=models.deletion.SET_DEFAULT)


class RelatedCousinModel(models.Model):
    related = models.ForeignKey(RelatedModel)
    null_related = models.ForeignKey(RelatedModel, blank=True, null=True)
    set_null_related = models.ForeignKey(
        RelatedModel,
        blank=True, null=True, on_delete=models.deletion.SET_NULL)
    set_default_related = models.ForeignKey(
        RelatedModel,
        blank=True, null=True, on_delete=models.deletion.SET_DEFAULT)


class RelatedArchiveModel(ArchiveMixin, models.Model):
    base = models.ForeignKey(BaseArchiveModel)
    null_base = models.ForeignKey(BaseArchiveModel, blank=True, null=True)
    set_null_base = models.ForeignKey(
        BaseArchiveModel,
        blank=True, null=True, on_delete=models.deletion.SET_NULL)
    set_default_base = models.ForeignKey(
        BaseArchiveModel,
        blank=True, null=True, on_delete=models.deletion.SET_DEFAULT)


class RelatedCousinArchiveModel(ArchiveMixin, models.Model):
    related = models.ForeignKey(RelatedArchiveModel)
    null_related = models.ForeignKey(
        RelatedArchiveModel, blank=True, null=True)
    null_related = models.ForeignKey(
        RelatedArchiveModel,
        blank=True, null=True, on_delete=models.deletion.SET_NULL)
    set_default_related = models.ForeignKey(
        RelatedArchiveModel,
        blank=True, null=True, on_delete=models.deletion.SET_DEFAULT)

