from django.contrib import admin
from core.models import AuditLogEntry, Notification, Enquiry, HomepageContent

admin.site.register(AuditLogEntry)
admin.site.register(Notification)
admin.site.register(Enquiry)
admin.site.register(HomepageContent)
