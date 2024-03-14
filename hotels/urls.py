from rest_framework_nested import routers
from . import views
from django.urls import path, include


router = routers.DefaultRouter()
router.register('hotels/(?P<city_name>[^/.]+)', views.CityHotelsViewSet, basename='city_hotels')
router.register('home', views.HomeViewSet, basename='home')

hotels_router = routers.NestedDefaultRouter(router, 'hotels/(?P<city_name>[^/.]+)')
hotels_router.register("rooms", views.RoomViewSet, basename="rooms")


urlpatterns = [
    path('', include(router.urls)),
    path('', include(hotels_router.urls)),
]