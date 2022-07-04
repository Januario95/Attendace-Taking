from django.db import models


class TableDeviceQuerySet(models.QuerySet):
    def serialize(self):
        list_values = list(self.values(
            'id', 'device_tag', 'device_mac', 'device_type',
            'device_status', 'device_assignment', 'device_temp',
            'device_o2', 'device_bat', 'device_hr', 'last_read_date',
            'last_read_time', 'incorrect_data_flag'))
        return list_values  # json.dumps(list_values, indent=4)


class TableDeviceManager(models.Manager):
    def get_queryset(self):
        return TableDeviceQuerySet(self.model, using=self._db)


class TableDevice(models.Model):
    device_tag = models.CharField(max_length=50, blank=True, null=True)
    device_mac = models.CharField(max_length=100, blank=True, null=True)
    device_type = models.CharField(max_length=100, default='HSWB004')
    device_status = models.CharField(max_length=20, blank=True, null=True)
    device_assignment = models.CharField(max_length=30, blank=True, null=True)
    device_temp = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    device_o2 = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    device_bat = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    device_hr = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    last_read_date = models.DateField(blank=True, null=True)
    last_read_time = models.TimeField(blank=True, null=True)
    incorrect_data_flag = models.IntegerField(default=0)

    objects = TableDeviceManager()

    def __str__(self):
        return self.device_mac

    class Meta:
        ordering = ('-device_status', '-last_read_date', '-last_read_time')
        verbose_name = 'Device'
        verbose_name_plural = 'Table Device'

    def serialize(self):
        data = {
            'id': self.id,
            'device_tag': self.device_tag,
            'device_mac': self.device_mac,
            'device_type': self.device_type,
            'device_status': self.device_status,
            'device_assignment': self.device_assignment,
            'device_temp': self.device_temp,
            'device_o2': self.device_o2,
            'device_bat': self.device_bat,
            'device_hr': self.device_hr,
            'last_read_date': self.device_hr,
            'last_read_time': self.last_read_time,
            'incorrect_data_flag': self.incorrect_data_flag
        }
        return data


class TblAlertCode(models.Model):
    # Field name made lowercase.
    alert_code = models.CharField(
        db_column='Alert_Code', primary_key=True, max_length=10)
    # Field name made lowercase.
    alert_description = models.CharField(
        db_column='Alert_Description', max_length=50)

    class Meta:
        verbose_name = 'Table Alert Code'
        verbose_name_plural = 'Table Alert Code'

    def __str__(self):
        return f'{self.alert_code}'


class TblDeviceRawLength(models.Model):
    # Field name made lowercase.
    device_type = models.CharField(
        db_column='Device_Type', primary_key=True, max_length=50)
    # Field name made lowercase.
    raw_data_length = models.IntegerField(db_column='Raw_Data_Length')

    class Meta:
        verbose_name = 'Table Device Raw Length'
        verbose_name_plural = 'Table Device Raw Length'

    def __str__(self):
        return f'{self.device_type}'


class TblGateway(models.Model):
    # Field name made lowercase.
    gateway_id = models.CharField(
        db_column='Gateway_ID', primary_key=True, max_length=50)
    # Field name made lowercase.
    gateway_location = models.CharField(
        db_column='Gateway_Location', max_length=50)
    # Field name made lowercase.
    gateway_address = models.CharField(
        db_column='Gateway_Address', max_length=50)
    # Field name made lowercase.
    gateway_mac = models.CharField(db_column='Gateway_Mac', max_length=50)
    # Field name made lowercase.
    gateway_serial_no = models.CharField(
        db_column='Gateway_Serial_No', max_length=50)
    # Field name made lowercase.
    gateway_topic = models.CharField(db_column='Gateway_Topic', max_length=50)
    # Field name made lowercase.
    gateway_latitude = models.CharField(
        db_column='Gateway_Latitude', max_length=50)
    # Field name made lowercase.
    gateway_longitude = models.CharField(
        db_column='Gateway_Longitude', max_length=50)
    # Field name made lowercase.
    gateway_type = models.CharField(db_column='Gateway_Type', max_length=50)
    device_tag = models.CharField(db_column='Device_Tag', max_length=50)
    last_updated_time = models.DateTimeField(auto_now=True)
    gateway_status = models.CharField(
        db_column='Gateway_Status', max_length=50)

    class Meta:
        ordering = ('-gateway_status',)
        verbose_name = 'Table Device Gateway'
        verbose_name_plural = 'Table Device Gateway'

    def __str__(self):
        return f'{self.gateway_id}'


class TableDeviceQuerySet(models.QuerySet):
    def serialize(self):
        list_values = list(self.values(
            'id', 'alert_code', 'alert_reading', 'alert_date',
            'alert_time', 'device_id', 'sent_to_crest',
            'alert_datetime'))
        return list_values


class TableDeviceManager(models.Manager):
    def get_queryset(self):
        return TableDeviceQuerySet(self.model, using=self._db)


class TableAlertQuerySet(models.QuerySet):
    def serialize(self):
        list_values = list(self.values(
            'id', 'alert_code', 'alert_reading', 'alert_date',
            'alert_time', 'device_id', 'sent_to_crest',
            'alert_datetime'))
        return list_values


class TableAlertManager(models.Manager):
    def get_queryset(self):
        return TableDeviceQuerySet(self.model, using=self._db)


class TableAlert(models.Model):
    alert_code = models.ForeignKey(
        to=TblAlertCode,
        on_delete=models.CASCADE
    )
    alert_reading = models.CharField(max_length=50)
    alert_date = models.DateField(auto_now=True)
    alert_time = models.TimeField(auto_now=True)
    device_id = models.ForeignKey(
        to=TableDevice, on_delete=models.CASCADE
    )
    sent_to_crest = models.IntegerField(default=0)
    alert_datetime = models.DateTimeField(auto_now=True)

    objects = TableAlertManager()

    def __str__(self):
        return f'{self.alert_code} - {self.alert_reading}'

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Table Alert'
        verbose_name_plural = 'Table Alert'

    def serialize(self):
        data = {
            'id': self.id,
            'alert_code': self.alert_code,
            'alert_reading': self.alert_reading,
            'alert_date': self.alert_date,
            'alert_time': self.alert_time,
            'device_id': self.device_id.device_mac,
            'sent_to_crest': self.sent_to_crest,
            'alert_datetime': self.alert_datetime
        }
        return data


class TableQuarantineQuerySet(models.QuerySet):
    def serialize(self):
        list_values = list(self.values(
            'id', 'device_tag', 'device_mac', 'device_type',
            'device_status', 'device_assignment', 'device_temp',
            'device_o2', 'device_bat', 'device_hr', 'last_read_date',
            'last_read_time', 'incorrect_data_flag'))
        return list_values  # json.dumps(list_values, indent=4)


class TableQuarantineManager(models.Manager):
    def get_queryset(self):
        return TableQuarantineQuerySet(self.model, using=self._db)


class TableQuarantine(models.Model):
    device_tag = models.CharField(max_length=50, blank=True, null=True)
    device_mac = models.CharField(max_length=100, blank=True, null=True)
    device_type = models.CharField(max_length=100, default='HSWB004')
    device_status = models.CharField(max_length=20, blank=True, null=True)
    device_assignment = models.CharField(max_length=30, blank=True, null=True)
    device_temp = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    device_o2 = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    device_bat = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    device_hr = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    last_read_date = models.DateField(blank=True, null=True)
    last_read_time = models.TimeField(blank=True, null=True)
    incorrect_data_flag = models.IntegerField(default=0)

    objects = TableQuarantineManager()

    def __str__(self):
        return self.device_mac

    class Meta:
        ordering = ('-device_status', '-last_read_date', '-last_read_time')
        verbose_name = 'Table Quarantine'
        verbose_name_plural = 'Table Quarantine'

    def serialize(self):
        data = {
            'id': self.id,
            'device_tag': self.device_tag,
            'device_mac': self.device_mac,
            'device_type': self.device_type,
            'device_status': self.device_status,
            'device_assignment': self.device_assignment,
            'device_temp': self.device_temp,
            'device_o2': self.device_o2,
            'device_bat': self.device_bat,
            'device_hr': self.device_hr,
            'last_read_date': self.device_hr,
            'last_read_time': self.last_read_time,
            'incorrect_data_flag': self.incorrect_data_flag
        }
        return data


class TableAllDevicesQuerySet(models.QuerySet):
    def serialize(self):
        list_values = list(self.values(
            'id', 'device_tag', 'device_mac', 'device_type',
            'device_status', 'device_assignment', 'device_temp',
            'device_o2', 'device_bat', 'device_hr', 'last_read_date',
            'last_read_time', 'incorrect_data_flag'))
        return list_values  # json.dumps(list_values, indent=4)


class TableAllDevicesManager(models.Manager):
    def get_queryset(self):
        return TableAllDevicesQuerySet(self.model, using=self._db)


class TableAllDevices(models.Model):
    device_tag = models.CharField(max_length=50, blank=True, null=True)
    device_mac = models.CharField(max_length=100, blank=True, null=True)
    device_type = models.CharField(max_length=100, default='HSWB004')
    device_status = models.CharField(max_length=20, blank=True, null=True)
    device_assignment = models.CharField(max_length=30, blank=True, null=True)
    device_temp = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    device_o2 = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    device_bat = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    device_hr = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    last_read_date = models.DateField(blank=True, null=True)
    last_read_time = models.TimeField(blank=True, null=True)
    incorrect_data_flag = models.IntegerField(default=0)

    objects = TableAllDevicesManager()

    def __str__(self):
        return self.device_mac

    class Meta:
        ordering = ('-device_status', '-last_read_date', '-last_read_time')
        verbose_name = 'Table Wearable'
        verbose_name_plural = 'Table Wearable'

    def serialize(self):
        data = {
            'id': self.id,
            'device_tag': self.device_tag,
            'device_mac': self.device_mac,
            'device_type': self.device_type,
            'device_status': self.device_status,
            'device_assignment': self.device_assignment,
            'device_temp': self.device_temp,
            'device_o2': self.device_o2,
            'device_bat': self.device_bat,
            'device_hr': self.device_hr,
            'last_read_date': self.device_hr,
            'last_read_time': self.last_read_time,
            'incorrect_data_flag': self.incorrect_data_flag
        }
        return data


class ScriptStatus(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    status = models.CharField(
        max_length=50, default='OFFLINE')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Script Status'
        verbose_name_plural = 'Script Status'
