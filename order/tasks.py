from celery import task

from django.core.mail import send_mail
from django.core.mail import EmailMessage

from io import BytesIO

from .models import Order
from .utils import write_invoice_pdf


@task
def send_order_created_email(pk, email, payment_url):
    subject = f'Order #{pk} was created'
    message = f'Order #{pk} was created. ' \
               'You can pay for it by clicking ' \
              f'on the following link: {payment_url}'
    from_email = "MineShop@gmail.com"

    email = EmailMessage(subject,
                          message,
                          from_email,
                          (email,))
    return email.send()


@task
def send_order_paid_email(pk):
    order = Order.objects.get(pk=pk)

    # Create PDF invoice
    out = BytesIO()
    write_invoice_pdf(out, pk)

    # Create email message
    subject = f'Order #{pk} was paid'
    message = f'Order #{pk} was paid. Please, check attachments to get invoice.'
    from_email = "MainShop@gmail.com"

    email = EmailMessage(subject,
                         message,
                         from_email,
                         (order.email,))

    # Attach pdf file to email
    email.attach(filename=f'invoice_{pk}.pdf',
                 content=out.getvalue(),
                 mimetype='application/pdf')

    # Send an email file
    email.send()
