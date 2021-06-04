from django.conf.urls import url
from .views import Order_Create, Admin_Order_Detail
from django.contrib.admin.views.decorators import staff_member_required

app_name = 'orders'
urlpatterns = [
    url(r'^create/$', Order_Create.as_view(), name='order_create'),
    url(r'^admin/order/(?P<order_id>\d+)/$', staff_member_required(Admin_Order_Detail.as_view()), name='admin_order_detail'),
]