from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import (
    TableDeviceViewSet, TblAlertCodeViewSet,
    TblDeviceRawLengthViewSet, TblGatewayViewSet,
    TableAlertViewSet,  TableQuarantineViewSet,
    TableAllDevicesViewSet,

    search_device_by_device_mac, update_device,
    filter_alert_by_code_and_device_id,
)

router = DefaultRouter()
router.register('tabledevice', TableDeviceViewSet)
router.register('alertcode', TblAlertCodeViewSet)
router.register('rawlength', TblDeviceRawLengthViewSet)
router.register('gateways', TblGatewayViewSet)
router.register('alerts', TableAlertViewSet)
router.register('quarantine', TableQuarantineViewSet)
router.register('alldevices', TableAllDevicesViewSet)

urlpatterns = [
    path('bluguard37/', include(router.urls)),
    path('update_device/', update_device),
    path('filter_alert_by_code_and_device_id/',
         filter_alert_by_code_and_device_id),
    path('search_device_by_device_mac/<str:device_mac>/',
         search_device_by_device_mac),
]
