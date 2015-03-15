from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views import generic
from payments import get_payment_model, RedirectNeeded

from app.models import RaceEvent, Order, Photo, OrderItem


def home(request):
    return render(request, 'app/home.html')

class RunnerView(generic.ListView):
    template_name = 'app/runner.html'
    context_object_name = 'races'

    def get_queryset(self):
        return RaceEvent.objects.all()

class TaggerView(generic.ListView):
    template_name = 'app/tagger.html'
    context_object_name = 'races'

    def get_queryset(self):
        return RaceEvent.objects.all()

class OrdersView(generic.ListView):
    template_name = 'app/orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user.id)

def photographer(request):
    return render(request, 'app/photographer.html')

def order_details(request, payment_id):
    payment = get_object_or_404(get_payment_model(), id=payment_id)
    payment.total = sum(p.price for p in payment.get_purchased_items())
    payment.save()
    try:
        form = payment.get_form(data=request.POST or None)
    except RedirectNeeded as redirect_to:
        return redirect(str(redirect_to))
    photos = Photo.objects.all()

    return TemplateResponse(request, 'app/order.html', {'form': form, 'payment': payment, 'photos': photos})


def order(request):
    photos = Photo.objects.all()
    Payment = get_payment_model()
    payment = Payment.objects.create(
        variant='stripe',  # this is the variant from PAYMENT_VARIANTS
        description='Photo purchase',
        total=0,
        tax=0,
        currency='USD',
        delivery=Decimal(0),
        billing_first_name=request.user.first_name,
        billing_last_name=request.user.last_name,
        billing_address_1='221B Baker Street',
        billing_address_2='',
        billing_city='London',
        billing_postcode='NW1 6XE',
        billing_country_code='UK',
        billing_country_area='Greater London',
        customer_ip_address='127.0.0.1')
    order = Order.objects.create(user=request.user, payment=payment)

    for photo in photos:
        OrderItem.objects.create(order=order, photo=photo, name=photo.name, sku='',
                            quantity=1, price=Decimal(7), currency='USD')

    return order_details(request, payment_id=payment.id)