from django.contrib import admin

from insurances.models import InsuranceMedical, InsuranceNotLeaving, Insurances


@admin.register(Insurances)
class InsuranceAdmin(admin.ModelAdmin):
    list_display = ("id", "medical", "not_leaving")


@admin.register(InsuranceMedical)
class InsuranceMedicalAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(InsuranceNotLeaving)
class InsuranceNotLeavingAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
