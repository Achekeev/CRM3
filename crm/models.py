from django.contrib.auth import get_user_model
from datetime import datetime
from django.db import models
import os

UserModel = get_user_model()


class City(models.Model):
    name = models.CharField('Город', max_length=255)

    def __str__(self):
        return self.name


class Website(models.Model):
    name = models.CharField('Сайт', max_length=255)
    url = models.CharField('URL Адрес', max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class ProfileWebsite(models.Model):
    website = models.ForeignKey(Website, verbose_name='Сайт', on_delete=models.CASCADE)
    url = models.CharField('URL Адрес', max_length=255, blank=True, null=True)
    login = models.CharField('Логин', max_length=255, blank=True, null=True)
    password = models.CharField('Пароль', max_length=255, blank=True, null=True)

    def __str__(self):
        return self.website.name


class CamModel(models.Model):
    name = models.CharField('ФИО', max_length=255)
    passport_scan = models.FileField('Скан паспорта', upload_to='model/passport/', blank=True, null=True)
    description = models.TextField('Описание', max_length=255, blank=True, null=True)
    schedule = models.TextField('Рассписание', max_length=255, blank=True, null=True)
    phone = models.CharField('Телефон', max_length=50, blank=True, null=True)
    email = models.CharField('Почта', max_length=255, blank=True, null=True)
    contacts = models.CharField('Доп. Контакты', max_length=255, blank=True, null=True)
    websites = models.ManyToManyField(ProfileWebsite, related_name='cammodels', verbose_name='Сайты', blank=True)
    percent = models.PositiveSmallIntegerField('Процент', default=25, blank=True)
    city = models.ForeignKey(City, verbose_name='Город', max_length=255, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self):
        return self.name

    def filled_today(self):
        if DailyTotal.objects.filter(cammodel_id=self.id, created_at__date=datetime.today()).exists():
            return True
        return False


class CamModelImage(models.Model):
    def get_image_path(self, filename):
        return f'model/images/{self.cammodel.id}-{self.cammodel.name}/{os.path.basename(filename)}'

    cammodel = models.ForeignKey(CamModel, verbose_name='Модель', related_name='images', on_delete=models.CASCADE)
    image = models.FileField('Фото', upload_to=get_image_path, blank=True, null=True)


class SupModel(models.Model):
    profile = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    username = models.CharField('Логин', max_length=255)
    password = models.CharField('Пароль', max_length=255)
    name = models.CharField('ФИО', max_length=255)
    phone = models.CharField('Телефон', max_length=50, blank=True, null=True)
    email = models.CharField('Почта', max_length=255, blank=True, null=True)
    contacts = models.CharField('Доп. Контакты', max_length=255, blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)


class CamModelRequest(models.Model):
    PENDING = 'pending'
    APPROVED = 'approved'
    DECLINED = 'declined'
    STATUS_CHOICES = ((PENDING, 'рассматривается'), (APPROVED, 'принято'), (PENDING, 'отказано'))

    name = models.CharField('ФИО', max_length=255)
    passport_scan = models.FileField('Скан паспорта', upload_to='model/passport/', blank=True, null=True)
    description = models.TextField('Предпочитаемый режим', max_length=255, blank=True, null=True)
    phone = models.CharField('Телефон', max_length=50, blank=True, null=True)
    email = models.CharField('Почта', max_length=255, blank=True, null=True)
    contacts = models.CharField('Доп. Контакты', max_length=255, blank=True, null=True)
    # status = models.CharField(max_length=255, choices=STATUS_CHOICES, default=PENDING, blank=True)
    created_at = models.DateTimeField('Дата заявки', auto_now_add=True)
    # request_uuid = models.CharField(max_length=255, blank=True, null=True)


class CamModelRequestImage(models.Model):
    def get_image_path(self, filename):
        return f'model/request/{self.request.id}-{self.request.name}/{os.path.basename(filename)}'

    request = models.ForeignKey(CamModelRequest, verbose_name='Заявка', related_name='images', on_delete=models.CASCADE)
    image = models.FileField('Фото', upload_to=get_image_path, blank=True, null=True)


class Operator(models.Model):
    name = models.CharField('ФИО', max_length=255)
    passport_scan = models.FileField('Скан паспорта', upload_to='operator/passport/', blank=True, null=True)
    image = models.FileField('Фото', upload_to='operator/images/', blank=True, null=True)
    birthday = models.DateField('Дата рождения', blank=True, null=True)
    work_place = models.CharField('Место работы', max_length=255, blank=True, null=True)
    percent = models.PositiveSmallIntegerField('Процент', default=25, blank=True)
    cammodel = models.OneToOneField(CamModel, on_delete=models.SET_NULL, verbose_name='Модель', blank=True, null=True)
    city = models.ForeignKey(City, verbose_name='Город', max_length=255, on_delete=models.SET_NULL, blank=True, null=True)
    websites = models.ManyToManyField(ProfileWebsite, related_name='operators', verbose_name='Сайты', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self):
        return self.name


class SupOperator(models.Model):
    profile = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    username = models.CharField('Логин', max_length=255)
    password = models.CharField('Пароль', max_length=255)
    name = models.CharField('ФИО', max_length=255)
    phone = models.CharField('Телефон', max_length=50, blank=True, null=True)
    email = models.CharField('Почта', max_length=255, blank=True, null=True)
    contacts = models.CharField('Доп. Контакты', max_length=255, blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)


class DailyTotal(models.Model):
    cammodel_id = models.PositiveIntegerField('ID Модели', blank=True)
    cammodel_name = models.CharField('ФИО Модели', max_length=255, blank=True, null=True)
    cammodel_amount = models.PositiveIntegerField('Доля Модели', default=0, blank=True)
    operator_id = models.PositiveIntegerField('ID Оператора', blank=True, null=True)
    operator_name = models.CharField('ФИО Оператора', max_length=255, blank=True, null=True)
    operator_amount = models.PositiveIntegerField('Доля Оператора', default=0, blank=True)
    website_id = models.PositiveIntegerField('ID Cайта', blank=True, null=True)
    website_name = models.CharField('Название сайта', max_length=255, blank=True, null=True)
    total = models.PositiveIntegerField('Итого', default=0, blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    def calculate_rate(self):
        if not self.cammodel_id:
            return
        cammodel = CamModel.objects.get(id=self.cammodel_id)
        cammodel_percent = cammodel.percent
        operator_percent = 0
        if self.operator_id:
            operator = Operator.objects.get(id=self.operator_id)
            operator_percent = operator.percent
        if self.total >= 1000:
            if cammodel_percent < 30:
                cammodel_percent += 5
            if operator_percent < 30:
                operator_percent += 5
        if self.total >= 2000:
            if cammodel_percent < 30:
                cammodel_percent += 5
            if operator_percent < 30:
                operator_percent += 5
        self.cammodel_amount = self.total / 100 * cammodel_percent
        if self.operator_id:
            self.operator_amount = self.total / 100 * operator_percent
