# Billing Daemon and DashBoard plugin

## Install (Temporary)

* Install Dashboard ( Same procedure as dashboard)
* git clone this project to the openstack-dashboard directory
* Add path of the the project directory to the nova
* Add flag to nova
  "--notification_driver=billing.billing_notifier"
* Configure path in dash_billing/bin/nova-notification
* add dash_billing.syspanel and dash_billing.dash for INSTALLED_APPS in dashbaord settings 
* launch nova and Billingdashboard and dash_billing/bin/nova-notification

#Example Settings
    INSTALLED_APPS = (
       'dashboard',
       'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django_openstack',
        'django_openstack.templatetags',
        'django.contrib.admin',
        'mailer',
        'dash_billing.syspanel', # <---
        'dash_billing.dash',  # <---
    )
