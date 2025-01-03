from django.contrib import admin

from .models import Amenity, Manager, Property

class ManagerAdmin(admin.ModelAdmin):
    search_fields = ('name', )

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'city', 'state', 'zip_code', 'rent', 'availability', 'manager')
    list_editable = ('rent', 'availability')
    list_per_page = 10
    search_fields = ('name', 'address', 'city')
    list_filter = ('availability', 'state', 'manager')
    ordering = ('state', 'name')

    filter_horizontal = ('amenities',)
    readonly_fields = ('address', 'city', 'state', 'zip_code')
    autocomplete_fields = ('manager', )

    actions = ('make_available', 'make_unavailable', 'raise_rent')

    @admin.action(description="Make select properties available")
    def make_available(self, request, queryset):
        queryset.update(availability=True)

    @admin.action(description="Make select properties unavailable")
    def make_unavailable(self, request, queryset):
        queryset.update(availability=False)

    @admin.action(description="Raise rent on selected properties by 10 percent")
    def raise_rent(self, request, queryset):
        for obj in queryset:
            obj.rent *= 1.1
            obj.save()

admin.site.register(Amenity)
admin.site.register(Manager, ManagerAdmin)
admin.site.register(Property, PropertyAdmin)
