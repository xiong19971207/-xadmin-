from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View

from apps.organizations.models import CourseOrg, City


class OrgListView(View):
    def get(self, request, *args, **kwargs):

        all_orgs = CourseOrg.objects.all()
        all_orgs_nums = CourseOrg.objects.count()
        all_citys = City.objects.all()

        return render(request, 'org-list.html', {
            'all_orgs': all_orgs,
            'all_citys': all_citys,
            'all_orgs_nums': all_orgs_nums,
        })
