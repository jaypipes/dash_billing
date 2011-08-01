## Nixon
### Nixon was framed...

Nixon is a django app/plugin/module written for OpenStack Dashboard. All it really does is allow you to include remote pages into the dashboard using iframes.

Nixon should be used as a skeleton example for drop-in applications to add functionality to the OpenStack Dashboard without requiring you to delve into the depths of the OpenStack Dashboard itself.

To make your app talk with OpenStack Dashboard, there are a few items you need to take care of in your __init__.py. To have links show up in your sidebar navigation you must customize the following items:

    MODULE_TITLE = "iFramer"
    LINKS = [
        {'url':'/syspanel/nixon/google', 'text':'Google', 'active_text': 'google'},
        # {'url':'http://google.com', 'text':'ffff'},
    ]

To get your app running in OpenStack Dashboard you must also add the application to INSTALLED_APPS in settings.py.

    INSTALLED_APPS = (
        ...
        'dashboard.nixon'
        ...
    )

