from rest_framework_nested import routers
from . import views
from django.urls import path, include


router = routers.DefaultRouter()

router.register('hotels/(?P<city_name>[^/.]+)', views.CityHotelsViewSet, basename='city_hotels')

router.register('home', views.HomeViewSet, basename='home')

urlpatterns = [
    path('', include(router.urls)),
    path('hotels/<slug:city_name>/<int:hotel_id>/rooms/', views.RoomsAPIView.as_view()),
    path('hotels/<slug:city_name>/<int:hotel_id>/rooms/<int:room_id>/', views.RoomAPIView.as_view()),
]
