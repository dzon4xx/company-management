from django.conf.urls import url
from rest_framework.schemas import get_schema_view
from employees import views


schema_view = get_schema_view(title='Company management API')


urlpatterns = [
    url(r'^$', views.api_root, name=views.api_root.__name__),
    url(r'^employees/$', views.EmployeeList.as_view(),
        name=views.EmployeeList.rev_name),

    url(r'^employees/(?P<email>[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)/$', views.EmployeeDetail.as_view(),
        name=views.EmployeeDetail.rev_name),

    url(r'^professions/$', views.ProfessionList.as_view(),
        name=views.ProfessionList.rev_name),

    url(r'^professions/(?P<pk>[0-9]+)/$', views.ProfessionDetail.as_view(),
        name=views.ProfessionDetail.rev_name),

    url('^schema/$', schema_view)
]
