from django.http import JsonResponse
from pure_pagination import Paginator, PageNotAnInteger
from django.shortcuts import render

from django.views.generic.base import View
from apps.organizations.models import CourseOrg, City
from apps.organizations.forms import AddAskForm


class AddAskView(View):
    """
    用户咨询页面的视图
    """

    def post(self, request, *args, **kwargs):
        user_ask_form = AddAskForm(request.POST)
        if user_ask_form.is_valid():
            user_ask_form.save(commit=True)
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "添加出错"
            })


class OrgListView(View):
    """
    授课机构的显示
    """

    def get(self, request, *args, **kwargs):

        all_orgs = CourseOrg.objects.all()
        all_citys = City.objects.all()
        # 根据收藏数显示机构
        hot_orgs = all_orgs.order_by('-fav_nums')[:3]

        # 根据机构查询
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 根据城市查询
        city_id = request.GET.get('city', '')
        if city_id:
            if city_id.isdigit():  # 判断对象是不是字符串
                all_orgs = all_orgs.filter(city_id=int(city_id))

        # 根据学生人数、课程数排序
        sort = request.GET.get('sort', '')
        if sort == 'students':
            all_orgs = all_orgs.order_by('-students')
        elif sort == 'courses':
            all_orgs = all_orgs.order_by('-course_nums')

        # 机构数量
        all_orgs_nums = all_orgs.count()

        # 设置分页器
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, per_page=3, request=request)
        # orgs是page对象，而不是queryset对象，前端调用要有object_list
        orgs = p.page(page)

        return render(request, 'org-list.html', {
            'all_orgs': orgs,
            'all_citys': all_citys,
            'all_orgs_nums': all_orgs_nums,
            'category': category,
            'city_id': city_id,
            'sort': sort,
            'hot_orgs': hot_orgs,
        })
