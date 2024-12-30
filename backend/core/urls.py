from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import (
    AnimalTypeViewSet,
    BreedViewSet,
    AnimalViewSet,
    WeightingViewSet,
    UserViewSet,
    register_user,
    login_user,
    AnimalList,
    welcome_view,
    activate_user,
    register_view,
    login_view,
    check_user_status
)

router = DefaultRouter()
router.register(r'animaltypes', AnimalTypeViewSet)
router.register(r'breeds', BreedViewSet)
router.register(r'animals', AnimalViewSet)
router.register(r'weightings', WeightingViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/register/', register_user, name='register_user'),
    path('register/', views.UserCreationView, name='register'),
    path('api/login/', login_user, name='login_user'),
    path('api/animals/', AnimalList.as_view(), name='animal_list'),
    path('api/welcome/', welcome_view, name='welcome'),
    path('api/activate/<str:uidb64>/<str:token>/', activate_user, name='activate_user'),
    path('admin/login/', login_view, name='login'),
    path('api/users/<int:pk>/toggle_active/', UserViewSet.as_view({'post': 'toggle_active'}), name='toggle_active'),
    path('weightings/', views.WeightingListView.as_view(), name='weighting_list'),
    path('weightings/edit/<int:id>/', views.edit_weighting, name='edit_weighting'),
    path('weightings/delete/<int:id>/', views.delete_weighting, name='delete_weighting'),
    path('api/user/status/', check_user_status, name='check_user_status')
]