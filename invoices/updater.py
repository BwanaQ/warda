from apscheduler.schedulers.background import BackgroundScheduler
from . import invoice_update

def start():
    scheduler = BackgroundScheduler(timezone="Africa/Nairobi")
    scheduler.add_job(invoice_update.monthly_invoicing_job, 'interval', seconds=10)
    scheduler.start()