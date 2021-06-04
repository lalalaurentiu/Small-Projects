import csv
import datetime
from django.http import HttpResponse
from django.contrib import admin
from .models import Order, OrderItem
from django.core import serializers
from django.urls import reverse

# Register your models here.

def export_as_json(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type="application/json")
    response['Content-Disposition'] = 'attachment; filename={}.json'.format(opts.verbose_name)
    serializers.serialize("json", queryset, stream=response)
    return response
export_as_json.short_description = 'Export to JSON'

def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)

    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    # write the header row
    writer.writerow([field.verbose_name for field in fields])
    #write data row
    for obj in queryset:
        datarow = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            datarow.append(value)
        writer.writerow(datarow)
    return response
export_to_csv.short_description = 'Export to CSV'

def order_detail(obj):
    return '<a href="{}">View</a>'.format(reverse('orders:admin_order_detail', args=[obj.id]))
order_detail.allow_tags = True

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', order_detail]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv, export_as_json]

admin.site.register(Order, OrderAdmin)