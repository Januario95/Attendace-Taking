from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views_new import (
    index, Quanrantine_Surveillance_Data,
    Online_Gateways_API, Lastest_Device_Data,
    fetch_user_info, top_five_alerts_api,
    update_user_info, Event_List, Attendee_List,
    Attendee_List_All,

    EventViewSet, AttendeeViewSet, AttendanceViewSet,
    TableDeviceViewSet,

    get_event_attendee, search_attended_by_gatewaymac,
    create_attendance,

    search_device_mac,
)

router = DefaultRouter()
router.register('events', EventViewSet)
router.register('attendee', AttendeeViewSet)
router.register('attendance', AttendanceViewSet)
router.register('tabledevice', TableDeviceViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('search_device_mac/<str:device_mac>/', search_device_mac),
    path('get_event_attendee/<int:event_id>/', get_event_attendee),
    path('search_attended_by_gatewaymac/<str:tag_id>/',
         search_attended_by_gatewaymac),
    path('create_attendance/<int:attendee_id>/<str:check_in>/<str:check_out>/',
         create_attendance),

    path('index/', index, name='index'),
    path('Quanrantine_Surveillance_Data/',
         Quanrantine_Surveillance_Data),
    path('online-gateways-api/', Online_Gateways_API),
    path('Lastest_Device_Data/', Lastest_Device_Data),
    path('fetch_user_info/', fetch_user_info),
    path('top_five_alerts_api/', top_five_alerts_api),
    path('update_user_info/<str:username>/<str:email>/',
         update_user_info),
    # path('events/', Event_List),
    # path('attendees/<str:Event_ID>/', Attendee_List),
    # path('attendee_list_all/', Attendee_List_All),
]
