from django.test import TestCase

from . import models


class ArchiveMixinTestCase(TestCase):

    def test_built_in_cascade(self):
        """
        Verifies cascade deletion
        """
        base = models.BaseModel.objects.create(name='test')
        models.NullRelatedModel.objects.create(nullable_base=base)

        base.delete()
        self.assertFalse(models.NullRelatedModel.objects.exists())

    def test_cascade_delete(self):
        """
        Verify that if we delete a model with the ArchiveMixin, then the
        delete cascades to its "parents", i.e. the models with foreign keys
        to it.
        """
        base = models.BaseArchiveModel.objects.create(name='test')
        related = models.RelatedModel.objects.create(base=base)
        models.RelatedCousinModel.objects.create(related=related)
        related_archivable = models.RelatedArchiveModel.objects.create(
            base=base)
        models.RelatedCousinArchiveModel.objects.create(
            related=related_archivable)

        base.delete()

        self.assertFalse(models.RelatedModel.objects.exists())
        self.assertFalse(models.RelatedCousinModel.objects.exists())
        self.assertFalse(models.RelatedArchiveModel.objects.exists())
        self.assertTrue(models.RelatedArchiveModel.all_objects.exists())
        self.assertFalse(models.RelatedCousinArchiveModel.objects.exists())
        self.assertTrue(models.RelatedCousinArchiveModel.all_objects.exists())

    def test_cascade_delete_qs(self):
        """
        Verify that if we delete a model with the ArchiveMixin, then the
        delete cascades to its "parents", i.e. the models with foreign keys
        to it.
        """
        base = models.BaseArchiveModel.objects.create(name='test')
        models.BaseArchiveModel.objects.create(name='test')
        models.BaseArchiveModel.objects.create(name='test')
        related = models.RelatedModel.objects.create(base=base)
        models.RelatedCousinModel.objects.create(related=related)
        related_archivable = models.RelatedArchiveModel.objects.create(
            base=base)
        models.RelatedCousinArchiveModel.objects.create(
            related=related_archivable)

        models.BaseArchiveModel.objects.all().delete()

        self.assertFalse(models.RelatedModel.objects.exists())
        self.assertFalse(models.RelatedCousinModel.objects.exists())
        self.assertFalse(models.RelatedArchiveModel.objects.exists())
        self.assertTrue(models.RelatedArchiveModel.all_objects.exists())
        self.assertFalse(models.RelatedCousinArchiveModel.objects.exists())
        self.assertTrue(models.RelatedCousinArchiveModel.all_objects.exists())

    def test_cascade_nullable(self):
        """
        Verify that related models are deleted even if the relation is
        nullable.
        """
        base = models.BaseArchiveModel.objects.create(name='test')
        base2 = models.BaseArchiveModel.objects.create(name='test2')
        related = models.RelatedModel.objects.create(
            base=base, null_base=base2)
        archivable_related = models.RelatedArchiveModel.objects.create(
            base=base, null_base=base2)
        models.RelatedCousinModel.objects.create(related=related)
        models.RelatedCousinArchiveModel.objects.create(
            related=archivable_related)

        base2.delete()

        self.assertEquals(1, models.BaseArchiveModel.objects.count())
        self.assertEquals(0, models.RelatedModel.objects.count())
        self.assertEquals(0, models.RelatedArchiveModel.objects.count())
        self.assertEquals(0, models.RelatedCousinModel.objects.count())
        self.assertEquals(0, models.RelatedCousinArchiveModel.objects.count())

    def test_cascade_set_null(self):
        """
        Verify that related models are not deleted if on_delete is SET_NULL
        """
        base = models.BaseArchiveModel.objects.create(name='test')
        base2 = models.BaseArchiveModel.objects.create(name='test2')
        related = models.RelatedModel.objects.create(
            base=base, set_null_base=base2)
        models.RelatedCousinModel.objects.create(related=related)

        base2.delete()

        self.assertEquals(1, models.BaseArchiveModel.objects.count())
        self.assertEquals(1, models.RelatedModel.objects.count())
        self.assertEquals(1, models.RelatedCousinModel.objects.count())

        self.assertTrue(
            models.RelatedModel.objects.filter(pk=related.pk).exists())

    def test_cascade_set_null_qs(self):
        """
        Verify that related models are not deleted if on_delete is SET_NULL
        """
        base = models.BaseArchiveModel.objects.create(name='test')
        base2 = models.BaseArchiveModel.objects.create(name='test2')
        related = models.RelatedModel.objects.create(
            base=base, set_null_base=base2)
        models.RelatedCousinModel.objects.create(related=related)

        models.BaseArchiveModel.objects.filter(pk=base2.pk).delete()

        self.assertEquals(1, models.BaseArchiveModel.objects.count())
        self.assertEquals(1, models.RelatedModel.objects.count())
        self.assertEquals(1, models.RelatedCousinModel.objects.count())

        self.assertTrue(
            models.RelatedModel.objects.filter(pk=related.pk).exists())

    def test_cascade_set_default(self):
        """
        Verify that related models are not deleted if on_delete is SET_DEFAULT
        """
        base = models.BaseArchiveModel.objects.create(name='test')
        base2 = models.BaseArchiveModel.objects.create(name='test2')
        related = models.RelatedModel.objects.create(
            base=base, set_default_base=base2)
        models.RelatedCousinModel.objects.create(related=related)

        base2.delete()

        self.assertEquals(1, models.BaseArchiveModel.objects.count())
        self.assertEquals(1, models.RelatedModel.objects.count())
        self.assertEquals(1, models.RelatedCousinModel.objects.count())

        self.assertTrue(
            models.RelatedModel.objects.filter(pk=related.pk).exists())
