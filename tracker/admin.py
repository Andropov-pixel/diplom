from django.contrib import admin

from users.models import User
from tracker.models import Tracker
from employee.models import Employee


admin.site.register(Tracker)

admin.site.register(Employee)

admin.site.register(User)