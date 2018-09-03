from django.conf.urls import url
from django.contrib.auth import views
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'App'

urlpatterns = [
    url(
        regex=r'^home/signup/',
        view=views.SignUp.as_view(),
        name='signup', #회원가입
    ),
    url(
        regex=r'home/list/create/',
        view=views.ListCreatePage.as_view(),
        name='list_create', # 리스트 생성 페이지
    ),
    url(
        regex=r'home/list/search/',
        view=views.ListSearchPage.as_view(),
        name='list_search', # 리스트 검색 페이지
    ), 
    url(
        regex=r'^home/list/(?P<post_id>[0-9]+)/',
        view=views.ListDetailPage.as_view(),
        name='post_detail', #리스트 디테일 페이지
    ),
    url(
        regex=r'home/list/',
        view=views.ListPage.as_view(),
        name='list', # 리스트페이지
    ),
    url(
        regex=r'home/',
        view=views.HomePage.as_view(),
        name='home', # 메인페이지
    ),
    url(
        regex=r'',
        view=views.StartPage.as_view(),
        name='start', # 시작페이지
    ), 
]



def ProjectListPage(request):
    search = request.GET.get('q')
    page = request.GET.get('page')
    if search == None:
        search = ""
    if page == None:
        page = 1

    projects = Project.objects.all()
    item_list = []
    for project in projects:
        dict = {}
        dict['project'] = project
        dict['apply'] = len(ProjectApply.objects.filter(project=project))
        dict['tags'] = ProjectTag.objects.filter(project=project)[:6]
        item_list.append(dict)

    paginator = Paginator(item_list, 3)
    contacts = paginator.get_page(page)

    return render(request, 'ProjectList/ProjectListPage.html', {
        'search': search,
        'page': page,
        'items': contacts,
        'projects_len':len(projects),
    })
