from datetime import datetime
from django.http.response import JsonResponse
from django.db.models import Sum
from invoices.models import Invoice
from service_management.models import ServiceRequest



def get_dashboard_data(request, *args, **kwargs):
    paid_invoices_this_month = Invoice.objects.filter(date_paid__month=datetime.now().month)
    paid_invoices_this_year = Invoice.objects.filter(date_paid__year=datetime.now().year)

    unpaid_invoices_this_month = Invoice.objects.filter(date_paid__month=datetime.now().month, paid=False)


    # calculate total amount paid this month using aggregate
    month_revenue = paid_invoices_this_month.aggregate(Sum('amount'))['amount__sum'] or 0

    # calculate total amount paid this year using aggregate
    annual_revenue = paid_invoices_this_year.aggregate(Sum('amount'))['amount__sum'] or 0

    # calculate total amount unpaid this month using aggregate
    month_unpaid_invoices = unpaid_invoices_this_month.aggregate(Sum('amount'))['amount__sum'] or 0

    # calculate total pending service_requests requests
    pending_maintainance_requests = ServiceRequest.objects.filter(status__name='Pending').count()

    months = [1,2,3,4,5,6,7,8,9,10,11,12]
    months_name = [
          "Jan",
          "Feb",
          "Mar",
          "Apr",
          "May",
          "Jun",
          "Jul",
          "Aug",
          "Sep",
          "Oct",
          "Nov",
          "Dec",
    ]
    # calculate total amount paid for each month from the months list above
    month_revenue_list = []

    for month in months:
        month_revenue_list.append(
            paid_invoices_this_month.filter(date_paid__month=month).aggregate(Sum('amount'))['amount__sum'] or 0
        )

    context = {
        'monthly_revenue': month_revenue,
        'annual_revenue': annual_revenue,
        'pending_maintainance_requests': pending_maintainance_requests,
        'unpaid_invoices_this_month': month_unpaid_invoices,
        'month_revenue_list': month_revenue_list,
        'labels': months_name,
        'dataset': month_revenue_list,
        "rent_collected_this_month": [month_unpaid_invoices,month_revenue ]
    
    }
    return JsonResponse(data=context)

def load_neighbour_data(request, *args, **kwargs):
    """loads Default Data for Neighbour"""
    from portfolio.utility import load_data
    context = {"data": load_data()}
    return JsonResponse(data=context)