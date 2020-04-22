from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from rest_framework import routers

from users.views import UserViewSet, UserSummaryView, TransactionViewSet, UserSummaryPerCategoryView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('users/<int:pk>/accounts-summary', UserSummaryView.as_view()),
    path('users/<int:pk>/transactions', TransactionViewSet.as_view()),
    path('users/<int:pk>/categorized', UserSummaryPerCategoryView.as_view())
]