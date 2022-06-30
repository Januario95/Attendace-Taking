from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (
    Event, Attendee,  Attendance,
    # TableDevice, TableAlert,
    TableBeacon,

    #     TblAcknowledgement, TblAlert, TblAlertCode,
    #     TblIncoming, TblSubscription, TblUser, TblCrestPatient,
    #     TblDailySurvey, TblDevice, TblDeviceRawLength,
    #     TblGateway, TblMessage, TblOrganization,
    #     TblWearer
)


@admin.register(TableBeacon)
class TableBeaconAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'serial_number',
                    'placement_location', 'last_battery_date',
                    'key', 'events']  # , 'view_events']

    def events(self, obj):
        # objs = [obj.event_name for obj in obj.event.all()]
        objs = [mark_safe(f"<li><a href='#'>{obj.event_name}</a></li>")
                for obj in obj.event.all()]
        news = ''
        for val in objs:
            news += val

        return mark_safe(f'<ol>{news}</ol>')
    events.short_description = 'View Events'

    def view_events(self, obj):
        return mark_safe(f'''
            <a href="#">View Event</a>
        ''')
    view_events.short_description = 'View Events'


# @ admin.register(TableAlert)
# class TableAlertAdmin(admin.ModelAdmin):
#     list_display = ['id', 'alert_code', 'alert_reading',
#                     'alert_date', 'alert_time',
#                     'device']


# @ admin.register(TableDevice)
# class TableDeviceAdmin(admin.ModelAdmin):
#     list_display = ['id', 'device_tag', 'device_mac', 'device_status',
#                     'device_assignment', 'device_temp', 'device_o2',
#                     'device_bat', 'device_hr', 'incorrect_data_flag',
#                     'last_read_date', 'last_read_time']


@ admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'event_name', 'start_datetime',
                    'end_datetime', 'event_location',
                    'event_sublocation',  # 'attendees_list',
                    'view_attendees']
    list_filter = ['tablebeacon']
    list_filter = ['event_name']
    # list_display_links = ['id', 'event_name']
    # list_editable = ['start_datetime', 'end_datetime']
    #  'event_name']

    def view_attendees(self, obj):
        url = f'/admin/apiapp/attendee/?event__id__exact={obj.id}'
        return mark_safe(f'''
            <a href="{url}">View Attendees Details</a>
        ''')
    view_attendees.short_description = 'View Attendees'

    def attendees_list(self, obj):
        objs = [mark_safe(f'<li>{obj.attendee_name}</li>')
                for obj in obj.attendee_set.all()]
        news = ''
        for val in objs:
            news += val

        return mark_safe(f'<ol>{news}</ol>')
    attendees_list.short_description = 'Attendees'


@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'attendee_name', 'tag_id',
                    # 'view_event',
                    'check_in_date', 'check_in_time',
                    'check_out_date', 'check_out_time',
                    'event_',
                    'last_updated', 'is_online']
    list_display_links = ['id', 'attendee_name']
    list_filter = ['event']
    # list_editable = ['check_in_date', 'check_in_time',
    #  'check_out_date', 'check_out_time']
    search_fields = ['event']

    def event_(self, obj):
        return mark_safe(f'''
            <a href="/admin/apiapp/event/">{obj.event}</a>
        ''')
    event_.short_description = 'View Event'


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['id', 'attendee', 'event',
                    'check_in_date', 'check_in_time',
                    'check_out_date', 'check_out_time']  # 'attendee', 'check_in_date',

    def event(self, obj):
        return obj.attendee.event
    event.short_description = 'Event'

    # def check_in_date(self, obj):
    #     date = obj.attendee.check_in_date
    #     return date
    # check_in_date.short_description = 'Check-in Date'

    # def check_in_time(self, obj):
    #     date = obj.attendee.check_in_time
    #     return date
    # check_in_time.short_description = 'Check-in Time'

    # def check_out_date(self, obj):
    #     date = obj.attendee.check_out_date
    #     return date
    # check_out_date.short_description = 'Check-out Date'

    # def check_out_time(self, obj):
    #     date = obj.attendee.check_out_time
    #     return date
    # check_out_time.short_description = 'Check-out Time'

# @admin.register(TblAcknowledgement)
# class TblAcknowledgementAdmin(admin.ModelAdmin):
#     list_display = ['ack_id', 'user',
#                     'ack_date', 'ack_time',
#                     'alert_id']


# @admin.register(TblAlert)
# class TblAlertAdmin(admin.ModelAdmin):
# 	list_display = ['alert_id', 'alert_code',
# 					'alert_reading', 'alert_date',
# 					'alert_time', 'device']


# @admin.register(TblAlertCode)
# class TblAlertCodeAdmin(admin.ModelAdmin):
#     list_display = ['alert_code', 'alert_description']


# @admin.register(TblIncoming)
# class TblIncomingAdmin(admin.ModelAdmin):
# 	list_display = ['incoming_id', 'incoming_device_mac',
#                     'incoming_gateway_mac', 'incoming_temp',
# 					'incoming_o2', 'incoming_hr',
# 					'incoming_date', 'incoming_time',
# 					'device_status', 'incorrect_data_flag',
# 					'device_bat_level', 'device_rssi']


# @admin.register(TblSubscription)
# class TblSubscriptionAdmin(admin.ModelAdmin):
# 	list_display = ['subscription_id', 'user',
# 					'device', 'subscription_created_date',
#                     'subscription_created_time']


# @admin.register(TblUser)
# class TblUserAdmin(admin.ModelAdmin):
# 	list_display = ['user_id', 'user_name',
# 					'user_email', 'user_login',
# 					'user_pwd', 'org_id']


# @admin.register(TblCrestPatient)
# class TblCrestPatientAdmin(admin.ModelAdmin):
#     list_display = ['patient_id', 'wearer',
#                     'patient_tag', 'band_tag',
#                     'created_date', 'created_time']


# @admin.register(TblDailySurvey)
# class TblDailySurveyAdmin(admin.ModelAdmin):
#     list_display = ['daily_survey_id', 'daily_survey_q1',
#                     'daily_survey_q2_y1', 'daily_survey_q2_y2',
#                     'daily_survey_q2_y3', 'daily_survey_q2_y4',
#                     'daily_survey_q2_y5', 'daily_survey_q3',
#                     'daily_survey_date', 'daily_survey_time',
#                     'daily_survey_session', 'wearer']


# @admin.register(TblDevice)
# class TblDeviceAdmin(admin.ModelAdmin):
#     list_display = ['device_id', 'device_type',
#                     'device_serial_no', 'device_mac',
#                     'device_bat_level', 'device_last_updated_date',
#                     'device_last_updated_time', 'wearer',
#                     'device_temp', 'device_hr',
#                     'device_o2', 'incoming_id',
#                     'device_rssi', 'gateway_mac',
#                     'incorrect_data_flag', 'device_status',
#                     'device_tag']


# @admin.register(TblDeviceRawLength)
# class TblDeviceRawLengthAdmin(admin.ModelAdmin):
#     list_display = ['device_type', 'raw_data_length']


# @admin.register(TblGateway)
# class TblGatewayAdmin(admin.ModelAdmin):
#     list_display = ['gateway_id', 'gateway_location',
#                     'gateway_address', 'gateway_mac',
#                     'gateway_serial_no', 'gateway_topic',
#                     'gateway_latitude', 'gateway_longitude',
#                     'gateway_type']


# @admin.register(TblMessage)
# class TblMessageAdmin(admin.ModelAdmin):
#     list_display = ['message_id', 'message_description',
#                     'message_date', 'message_time',
#                     'message_type', 'user',
#                     'wearer_id']


# @admin.register(TblOrganization)
# class TblOrganizationAdmin(admin.ModelAdmin):
#     list_display = ['org_id', 'org_name',
#                     'org_rep', 'org_rep_email',
#                     'org_address']


# @admin.register(TblWearer)
# class TblWearerAdmin(admin.ModelAdmin):
#     list_display = ['wearer_id', 'wearer_nick',
#                     'wearer_pwd']
