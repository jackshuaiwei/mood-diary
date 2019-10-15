from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from .models import Record
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.
def index(request):
    return render(request, 'record/index.html')

@login_required(login_url='/userprofile/login/')
def detail(request, id):
    if request.user.id != id:
        return HttpResponse("你没有权限访问别人的主页")
    else:
        num = request.GET.get('num')
        record = Record.objects.get(Q(user_id=id), Q(id=num))
        day = timezone.now().day
        month = timezone.now().month
        mon_list = [
            'January', 'February', 'March', 'April', 'May',
            'June', 'July', 'August', 'September',
            'October', 'November','December'
        ]
        context = {'record':record,"day":day,"month":mon_list[month-1]}

        return render(request, 'record/detail.html', context)