from django.contrib import admin

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'created_at']
    list_editable = ['status']