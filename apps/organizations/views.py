from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View

from apps.organizations.models import CourseOrg, City


class OrgListView(View):
    def get(self, request, *args, **kwargs):

        all_orgs = CourseOrg.objects.all()
        all_orgs_nums = CourseOrg.objects.count()
        all_citys = City.objects.all()

        # 设置分页器
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs,per_page=3, request=request)
        # orgs是page对象，而不是queryset对象，前端调用要有object_list
        orgs = p.page(page)

        return render(request, 'org-list.html', {
            'all_orgs': orgs,
            'all_citys': all_citys,
            'all_orgs_nums': all_orgs_nums,
        })
