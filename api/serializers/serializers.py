from rest_framework import serializers
from core.models import RasterImage

class RasterImageSerializer(serializers.ModelSerializer):  
    class Meta:
        model = RasterImage
        # fields = "__all__"
        exclude=("filename","extension")
