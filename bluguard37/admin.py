from django.contrib import admin

from .models import (
    TblAlertCode, TblDeviceRawLength, TblGateway,
    TableDevice, TableAlert, TableQuarantine,
    TableAllDevices, ScriptStatus
)


@admin.register(ScriptStatus)
class ScriptStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'status', 'description']


@admin.register(TableAlert)
class TableAlertAdmin(admin.ModelAdmin):
    list_display = ['id', 'alert_code', 'alert_reading', 'alert_date',
                    'alert_time', 'device_id', 'sent_to_crest',
                    'alert_datetime']
    ordering = ['-id', ]


@admin.register(TableAllDevices)
class TableAllDevicesAdmin(admin.ModelAdmin):
    list_display = ['id', 'device_tag', 'device_mac', 'device_type',
                    'device_status', 'device_assignment', 'device_temp',
                    'device_o2', 'device_bat', 'device_hr',
                    'incorrect_data_flag',
                    'last_read_date', 'last_read_time']
    list_per_page = 15
    ordering = ['id']
    search_fields = ['device_mac', ]


@admin.register(TableQuarantine)
class TableQuarantineAdmin(admin.ModelAdmin):
    list_display = ['id', 'device_tag', 'device_mac', 'device_type',
                    'device_status', 'device_assignment', 'device_temp',
                    'device_o2', 'device_bat', 'device_hr',
                    'incorrect_data_flag',
                    'last_read_date', 'last_read_time']


@admin.register(TableDevice)
class TableDeviceAdmin(admin.ModelAdmin):
    list_display = ['id', 'device_tag', 'device_mac', 'device_type',
                    'device_status', 'device_assignment', 'device_temp',
                    'device_o2', 'device_bat', 'device_hr',
                    'incorrect_data_flag',
                    'last_read_date', 'last_read_time']


@admin.register(TblAlertCode)
class TblAlertCodeAdmin(admin.ModelAdmin):
    list_display = ['alert_code', 'alert_description']
    list_display_links = ['alert_code']


@admin.register(TblDeviceRawLength)
class TblDeviceRawLengthAdmin(admin.ModelAdmin):
    list_display = ['device_type', 'raw_data_length']


@admin.register(TblGateway)
class TblGatewayAdmin(admin.ModelAdmin):
    # list_display = ['gateway_id', 'gateway_location',
    list_display = ['gateway_location',
                    'gateway_address', 'gateway_mac',
                    'gateway_serial_no', 'gateway_topic',
                    'gateway_latitude', 'gateway_longitude',
                    'gateway_type', 'device_tag', 'last_updated_time',
                    'gateway_status']
