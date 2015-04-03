from decimal import Decimal
from django.core.files.base import ContentFile
from django.contrib import messages
from json import load
from urllib import urlopen

from boto.s3.bucket import Bucket
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import os
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views import generic
from django.views.decorators.http import require_POST
from jfu.http import upload_receive, UploadResponse, JFUResponse
from payments import get_payment_model, RedirectNeeded

from app.forms import RaceListFormHelper, NewRaceForm
from app.models import RaceEvent, Order, Photo, OrderItem
from forty_two_k import settings
from raceFuncs import RaceFilter, RaceTable


from django.shortcuts import render_to_response
from django.template import RequestContext

from django.contrib.auth.decorators import login_required


def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response


def home(request):
    return render(request, 'app/home.html')


def terms(request):
    return render(request, 'app/tnc.html')


def support(request):
    return render(request, 'app/support.html')


def feedback(request):
    return render(request, 'app/feedback.html')


def login(request):
    return render(request, 'app/login.html')


@login_required
def RunnerOverview(request):
    return render(request, 'app/runner-overview.html')


@login_required
def RunnerInputbib(request):
    return render(request, 'app/runner-inputbib.html')


class TaggerView(generic.ListView):
    template_name = 'app/tagger.html'
    context_object_name = 'races'

    def get_queryset(self):
        return RaceEvent.objects.all()


@login_required
def tag(request):
    return render(request, 'app/tag.html')


class OrdersView(generic.ListView):
    template_name = 'app/orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user.id)



class UploadView(generic.TemplateView):
    template_name = 'app/upload.html'

    def get_context_data(self, **kwargs):
        context = super( UploadView, self ).get_context_data( **kwargs )
        context['accepted_mime_types'] = ['image/*']
        context['races'] = RaceEvent.objects.all()
        album = self.request.REQUEST.get('album')
        if album:
            token = self.request.user.app.facebooktoken
            context['photos'] = load(urlopen(
                'https://graph.facebook.com/%s/photos?access_token='
                % album + token))
        elif 'facebook' in self.request.REQUEST:
            token = self.request.user.app.facebooktoken
            context['albums'] = albums = load(urlopen(
                'https://graph.facebook.com/me/albums?access_token=' + token))
            if 'error' in albums:
                raise RuntimeError(
                    albums['error'])  # TODO: replace with messages
        return context

    def post(self, request):
        album = self.request.REQUEST.get('album')
        token = self.request.user.app.facebooktoken
        photos = load(urlopen(
            'https://graph.facebook.com/%s/photos?access_token='
            % album + token))
        for p in photos['data']:
            if self.request.REQUEST['upload-' + p['id']] == 'on':
                race = RaceEvent.objects.get(
                    pk=self.request.REQUEST['race-' + p['id']])
                Photo.objects.create(file=ContentFile(urlopen(
                    p['source']).read(), name='photo.jpg'), race=race)
        messages.success(request, 'Photos added.')
        return redirect('/')


@login_required
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


@login_required
def order(request):
    photos = Photo.objects.all()
    Payment = get_payment_model()
    payment = Payment.objects.create(
        variant='stripe',  # this is the variant from PAYMENT_VARIANTS
        description='Photo purchase',
        total=1,
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
        OrderItem.objects.create(order=order, photo=photo, name=photo.file.path, sku='',
                            quantity=1, price=Decimal(7), currency='USD')

    return order_details(request, payment_id=payment.id)



@require_POST
def upload(request):

    # The assumption here is that jQuery File Upload
    # has been configured to send files one at a time.
    # If multiple files can be uploaded simulatenously,
    # 'file' may be a list of files.
    file = upload_receive( request )
    raceid = request.POST.get("raceevent", "")
    raceevent = RaceEvent.objects.get(id=raceid)
    instance = Photo(file=file, race=raceevent)
    instance.save()

    basename = os.path.basename( instance.file.path )
    file_dict = {
        'name' : basename,
        'size' : file.size,

        'url': instance.file.url,
        'thumbnailUrl': instance.file.url,

        'deleteUrl': reverse('jfu_delete', kwargs = { 'pk': instance.pk }),
        'deleteType': 'POST',
    }

    return UploadResponse( request, file_dict )

@require_POST
def upload_delete(request, pk):
    success = True
    try:
        instance = Photo.objects.get( pk = pk )

        conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
        b = Bucket(conn, settings.AWS_STORAGE_BUCKET_NAME)
        k = Key(b)
        k.key = instance.file.path
        b.delete_key(k)

        instance.delete()
    except Photo.DoesNotExist:
        success = False

    return JFUResponse(request, success)



from django_tables2 import SingleTableView


class PagedFilteredTableView(SingleTableView):
    filter_class = None
    formhelper_class = None
    context_filter_name = 'filter'

    def get_queryset(self, **kwargs):
        qs = super(PagedFilteredTableView, self).get_queryset()
        self.filter = self.filter_class(self.request.GET, queryset=qs)
        self.filter.form.helper = self.formhelper_class()
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super(PagedFilteredTableView, self).get_context_data()
        context[self.context_filter_name] = self.filter
        context['new_race_form'] = NewRaceForm
        context['races'] = RaceEvent.objects.all()
        return context


class RunnerView(PagedFilteredTableView):
    model = RaceEvent
    table_class = RaceTable
    template_name = 'app/runner.html'
    filter_class = RaceFilter
    formhelper_class = RaceListFormHelper
    formhelper_class.field_template = 'bootstrap3/layout/inline_field.html'
    formhelper_class.form_class = 'form-inline'


@login_required
def addRace(request):
    if request.POST:
        name = request.POST['name']
        date = request.POST['date']
        city = request.POST['city']
        country = request.POST['country']

        RaceEvent.objects.create(name=name, date=date, city=city, country=country, submitted_by=request.user, validated_by=request.user)

        return redirect('runner')

