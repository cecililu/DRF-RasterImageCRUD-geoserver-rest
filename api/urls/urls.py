from django.urls import include, path
from rest_framework import routers

from api.viewsets.viewsets import RasterImageViewset

router = routers.SimpleRouter()
router.register(r'rasterimage', RasterImageViewset)

urlpatterns = [
    path('', include(router.urls)),
 
]