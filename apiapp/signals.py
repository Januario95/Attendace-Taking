from django.dispatch import receiver
from django.db.models.signals import (
    pre_save, post_save
)

from .models import (
    Event, Attendee, Attendance,
    TableDevice, TableAlert
)


@receiver(pre_save, sender=Attendee)
def attendee_pre_save(sender, instance,
                      *args, **kwargs):
    # print(f'instance = {instance}')
    print('pre-save\n')


@receiver(post_save, sender=Attendee)
def attendee_post_save(sender, instance,
                       created, *args, **kwargs):
    if created:
        print('CREATED')
    else:
        print('SAVED')
        # obj = Attendance.objects.create(attendee=instance)
        # obj.save()
