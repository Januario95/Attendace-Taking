from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import (
    TableDeviceViewSet, TblAlertCodeViewSet,
    TblDeviceRawLengthViewSet, TblGatewayViewSet,
    TableAlertViewSet,  TableQuarantineViewSet,
    TableAllDevicesViewSet, ScriptStatussViewSet,

    search_device_by_device_mac, update_device,
    filter_alert_by_code_and_device_id,
    get_all_alerts, clear_all_alerts,
)

router = DefaultRouter()
router.register('tabledevice', TableDeviceViewSet)
router.register('alertcode', TblAlertCodeViewSet)
router.register('rawlength', TblDeviceRawLengthViewSet)
router.register('gateways', TblGatewayViewSet)
router.register('alerts', TableAlertViewSet)
router.register('quarantine', TableQuarantineViewSet)
router.register('alldevices', TableAllDevicesViewSet)
router.register('scripts', ScriptStatussViewSet)

urlpatterns = [
    path('clear_all_alerts/', clear_all_alerts),
    path('get_all_alerts/', get_all_alerts),
    path('bluguard37/', include(router.urls)),
    path('update_device/', update_device),
    path('filter_alert_by_code_and_device_id/',
         filter_alert_by_code_and_device_id),
    path('search_device_by_device_mac/<str:device_mac>/',
         search_device_by_device_mac),
]
