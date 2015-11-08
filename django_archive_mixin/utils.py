from distutils.version import StrictVersion

import django
from django.db import models
from django.utils import timezone


def get_field_by_name(model, field):
    """
    Retrieve a field instance from a model by its name.
    """
    field_dict = {x.name: x for x in model._meta.get_fields()}

    return field_dict[field]


def cascade_archive(inst_or_qs, using, keep_parents=False):
    """
    Return collector instance that has marked ArchiveMixin instances for
    archive (i.e. update) instead of actual delete.

    Arguments:
        inst_or_qs (models.Model or models.QuerySet): the instance(s) that
            are to be deleted.
        using (db connection/router): the db to delete from.
        keep_parents (bool): defaults to False.  Determine if cascade is true.

    Returns:
        models.deletion.Collector: this is a standard Collector instance but
            the ArchiveMixin instances are in the fields for update list.
    """
    from common.models.mixins import ArchiveMixin, ActiveArchiveMixin

    if not isinstance(inst_or_qs, models.QuerySet):
        instances = [inst_or_qs]
    else:
        instances = inst_or_qs

    deleted_ts = timezone.now()

    # The collector will iteratively crawl the relationships and
    # create a list of models and instances that are connected to
    # this instance.
    collector = models.deletion.Collector(using=using)
    if StrictVersion(django.get_version()) < StrictVersion('1.9.0'):
        collector.collect(instances)
    else:
        collector.collect(instances, keep_parents=keep_parents)
    collector.sort()

    for model, instances in collector.data.iteritems():
        # remove archive mixin models from the delete list and put
        # them in the update list.  If we do this, we can just call
        # the collector.delete method.
        inst_list = list(instances)
        if issubclass(model, ActiveArchiveMixin):
            active_field = get_field_by_name(model, 'active')
            collector.add_field_update(active_field, False, inst_list)

        if issubclass(model, (ArchiveMixin, ActiveArchiveMixin)):
            deleted_on_field = get_field_by_name(model, 'deleted_on')
            collector.add_field_update(
                deleted_on_field, deleted_ts, inst_list)

            del collector.data[model]

    for i, qs in enumerate(collector.fast_deletes):
        # make sure that we do archive on fast deletable models as
        # well.
        model = qs.model

        if issubclass(model, ActiveArchiveMixin):
            active_field = get_field_by_name(model, 'active')
            collector.add_field_update(active_field, False, qs)

        if issubclass(model, (ArchiveMixin, ActiveArchiveMixin)):
            deleted_on_field = get_field_by_name(model, 'deleted_on')
            collector.add_field_update(deleted_on_field, deleted_ts, qs)

            collector.fast_deletes[i] = qs.none()

    return collector
