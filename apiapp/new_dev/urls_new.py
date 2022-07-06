from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views_new import (
    index,
    #     Quanrantine_Surveillance_Data,
    #     Online_Gateways_API, Lastest_Device_Data,
    #     fetch_user_info, top_five_alerts_api,
    #     update_user_info, Event_List, Attendee_List,
    #     Attendee_List_All,

    EventViewSet, AttendeeViewSet, AttendanceViewSet,
    TableDeviceViewSet, TableBeaconViewSet,

    delete_event, set_device_offline_online,
    get_event_attendee, search_attended_by_gatewaymac,
    create_attendance, update_attendance,
    set_event_active_inactive, get_attendance_by_attendee_id,

    search_device_mac, search_attendee_by_id,
    search_attendance, check_out_attendance,
    get_event_name, delete_all_attendance,
    delete_all_attendance_by_event,
)

router = DefaultRouter()
router.register('events', EventViewSet)
router.register('attendee', AttendeeViewSet)
router.register('attendance', AttendanceViewSet)
router.register('tabledevice', TableDeviceViewSet)
router.register('beacons', TableBeaconViewSet)


urlpatterns = [
     path('', include(router.urls)),
     path('get_attendance_by_attendee_id/<int:attendee_id>/',
          get_attendance_by_attendee_id),
     path('set_event_active_inactive/<int:event_id>/<str:event_name>/',
          set_event_active_inactive,),
     path('delete_all_attendance_by_event/<int:event_id>/',
          delete_all_attendance_by_event),
     path('delete_all_attendance/', delete_all_attendance),
     path('delete_event/<int:event_id>/', delete_event),
     path('set_device_offline_online/', set_device_offline_online),
     path('get_event_name/<int:event_id>/', get_event_name),
     path('check_out_attendance/<int:attendance_id>/<str:check_out_date>/<str:check_out_time>/',
          check_out_attendance),
     path('search_attendance/<str:attendee_name>/<str:check_in_date>/<str:check_in_time>/',
          search_attendance),
     path('search_attendee_by_id/<str:attendee_id>/', search_attendee_by_id),
     path('search_device_mac/<str:device_mac>/', search_device_mac),
     path('get_event_attendee/<int:event_id>/', get_event_attendee),
     path('search_attended_by_gatewaymac/<str:tag_id>/',
          search_attended_by_gatewaymac),
     path('create_attendance/<str:tag_id>/<int:event_id>/<str:check_in_date>/<str:check_in_time>/',  # <str:check_out_date>/<str:check_out_time>/',
          create_attendance),
     path('update_attendance/<str:attendee>/<str:check_in_date>/<str:check_in_time>/<str:check_out_date>/<str:check_out_time>/',
          update_attendance),

     path('index/', index, name='index'),
    #     path('Quanrantine_Surveillance_Data/',
    #          Quanrantine_Surveillance_Data),
    #     path('online-gateways-api/', Online_Gateways_API),
    #     path('Lastest_Device_Data/', Lastest_Device_Data),
    #     path('fetch_user_info/', fetch_user_info),
    #     path('top_five_alerts_api/', top_five_alerts_api),
    #     path('update_user_info/<str:username>/<str:email>/',
    #          update_user_info),
    # path('events/', Event_List),
    # path('attendees/<str:Event_ID>/', Attendee_List),
    # path('attendee_list_all/', Attendee_List_All),
]
