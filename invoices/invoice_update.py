from datetime import datetime
from django.conf import settings
from application_and_lease_management.models import UnitLease
from invoices.models import Invoice


import africastalking
import os
# Initialize SDK
username = os.environ.get('AFRICASTALKING_USER_NAME') 
api_key = os.environ.get('AFRICASTALKING_API_KEY')

print(username)

africastalking.initialize(username, api_key)

sms = africastalking.SMS

def monthly_invoicing_job():
    """Function to run monthly invoicing job and send notification to tenant on mobile phone
    TODO: Add logging in the future
    """
    leases = UnitLease.objects.filter(is_active=True)
    invoice_code = 'INV-'+str(datetime.now().date())
    last_invoice_id = None
    

    for lease in leases:
        # Check if lease has invoice next month 
        if Invoice.objects.filter(unitlease=lease, month=datetime.now().month + 1).exists() is False:
            last_invoice = Invoice.objects.all().order_by('-date_created').first()
            if last_invoice is not None:
                last_invoice_id = last_invoice.id
            else:
                last_invoice_id = 0
            
            if lease.is_first_time:
                try:
                    invoice = Invoice.objects.create(
                        building_id = lease.unit.building.id,
                        unitlease=lease,
                        month=datetime.now().month+1,
                        description=f'First time rent for {lease.unit.name}',
                        date_created=datetime.now(),
                        date_due=f'{datetime.now().year}-{datetime.now().month+1}-05',
                        amount=lease.deposit + lease.rent,
                        paid=False,
                        invoice_no=f'{invoice_code}{last_invoice_id +1}'
                    )
                    lease.is_first_time = False
                    lease.save()

                    # When invoice is created, send sms to tenant
                    tenant = lease.application.tenant
                    invoice_message=f'Hello, {tenant.user.first_name}, your rent payment of shs {invoice.amount} is due on demand. Please plan to pay before 5th.'
                    response =sms.send(invoice_message, [str(tenant.phone_number)])
                    print(response)
                except Exception as e:
                    print(str(e))
            
            else:
                last_invoice = Invoice.objects.all().order_by('-date_created').first()
                invoice = Invoice.objects.create(
                    unitlease=lease,
                    building_id = lease.unit.building.id,
                    month=datetime.now().month+1,
                    description=f'Rent for {lease.unit.name}',
                    date_created=datetime.now(),
                    date_due=f'{datetime.now().year}-{datetime.now().month+1}-05',
                    amount=lease.rent,
                    paid=False,
                    invoice_no=f'{invoice_code}{last_invoice_id +1}'
                )

                print(f'Created invoice for {lease.unit}')
                # When invoice is created, send sms to tenant
                tenant = lease.application.tenant
                invoice_message=f'Hello, {tenant.user.first_name}, your rent payment of shs {invoice.amount} is due on demand. Please plan to pay before 5th.'
                response =sms.send(invoice_message, [str(tenant.phone_number)])
                print(response)
        else:
            print(f'Invoice for {lease.unit} already exists for next month')
            continue

