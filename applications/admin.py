from django.contrib import admin

from applications.models import Application


@admin.register(Application)
class AdminApplication(admin.ModelAdmin):
    """
    Админ панель для модели Application
    """
    pass