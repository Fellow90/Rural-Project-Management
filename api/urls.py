from django.urls import path,include
from api import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'project',viewset= views.ProjectViewSet, basename = 'project')
router.register(r'excel',viewset= views.ExcelViewSet, basename = 'excel')
router.register(r'province',views.ProvinceViewSet, basename='province')
router.register(r'district',views.DistrictViewSet, basename='district')
router.register(r'municipality',views.MunicipalityViewSet, basename='municipality')

urlpatterns = [
    path('',include(router.urls)),
]