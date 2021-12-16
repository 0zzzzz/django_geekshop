import base64
from hashlib import md5

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import mail_admins
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from interkassaapp.forms import NotificationForm, SettledPaymentForm, PaymentRequestForm
from interkassaapp.models import Invoice, Payment
from interkassaapp.signals import interkassa_payment_accepted


@require_POST
@csrf_exempt
def result(request):
    form = NotificationForm(request.POST)
    if not form.is_valid():
        message = 'Invalid Form Data:\n'
        for key in form.errors:
            message += key + ', '.join(form.errors[key]) + '\n'
        mail_admins('Unprocessed request to interkassa merchant',
                    message, fail_silently=True)
        return HttpResponseBadRequest("Invalid Form Data!")

    if form.cleaned_data['ik_act'] not in ('process', ''):
        mail_admins('Unprocessed request to interkassa merchant',
                    'Status: "%s"' % form.cleaned_data['ik_act'], fail_silently=True)
        return HttpResponse("success")

    payment_no = form.cleaned_data['ik_pm_no']
    try:
        invoice = Invoice.objects.get(payment_no=payment_no)
    except ObjectDoesNotExist:
        mail_admins('Unprocessed request to interkassa merchant',
                    'Not found Invoice with payment_no=%s' % payment_no, fail_silently=True)
        return HttpResponseBadRequest("Invalid Invoice ID!")

    data = []
    for x in sorted(request.POST.keys()):
        if x.startswith('ik_') and x != 'ik_sign':
            data.append(str(request.POST.get(x)))
    data.append(settings.INTERKASSA_SECRET)
    sign = base64.b64encode(md5(":".join(data).encode()).digest()).decode()

    if form.cleaned_data['ik_sign'] == sign:
        amount = form.cleaned_data['ik_am']
        if amount != invoice.amount:
            mail_admins('Unprocessed request to interkassa merchant',
                        'Incorrect ik_am=%s for payment_no=%s' % (amount, payment_no),
                        fail_silently=True)
            return HttpResponseBadRequest("Incorrect ik_am")

        if form.cleaned_data['ik_inv_st'] == 'success':
            payment = Payment(amount=amount, invoice=invoice, payment_no=payment_no,
                              ik_pw_via=form.cleaned_data['ik_pw_via'],
                              ik_cur=form.cleaned_data['ik_cur'],
                              ik_inv_prc=form.cleaned_data['ik_inv_prc'])
            payment.save()
            interkassa_payment_accepted.send(sender=payment.__class__, payment=payment)
        else:
            message = 'Status ik_inv_st was %s for payment_no=%s' % (form.cleaned_data['ik_inv_st'],
                                                                     payment_no)
            mail_admins('Unprocessed request to interkassa merchant',
                        message, fail_silently=True)
        return HttpResponse("success")
    else:
        mail_admins('Unprocessed request to interkassa merchant',
                    'Incorrect hash for payment %s.' % payment_no, fail_silently=True)
        return HttpResponseBadRequest("Incorrect hash")


@csrf_exempt
def success(request):
    response = {}
    form = SettledPaymentForm(request.POST)
    if form.is_valid():
        response = form.cleaned_data
    return render(request, 'interkassaapp/success.html', response)


@csrf_exempt
def fail(request):
    response = {}
    form = SettledPaymentForm(request.POST)
    if form.is_valid():
        response = form.cleaned_data
    return render(request, 'interkassaapp/fail.html', response)


@csrf_exempt
def wait(request):
    return render(request, 'interkassaapp/wait.html', {})


@login_required
def balance(request):
    default_amount = 300
    if request.method == 'POST':
        amount = request.POST.get('amount')
        if amount:
            try:
                amount = int(amount)
            except Exception:
                amount = default_amount
        else:
            amount = default_amount
        inv = Invoice.objects.create(amount=amount, user=request.user,
                                     payment_info='Пополнение баланса')
        initial = dict(ik_co_id=settings.INTERKASSA_ID, ik_pm_no=inv.payment_no,
                       ik_am=inv.amount, ik_desc=inv.payment_info)
        form = PaymentRequestForm(initial=initial)
    else:
        form = PaymentRequestForm()
    return render(request, 'interkassaapp/balance.html', locals())
