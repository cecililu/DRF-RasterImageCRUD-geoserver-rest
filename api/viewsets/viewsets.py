from django.shortcuts import render
from rest_framework import viewsets
from geo.Geoserver import Geoserver
from django.conf import settings
from core.models import RasterImage
from rest_framework.response import Response
from api.serializers.serializers import RasterImageSerializer
import os

geoserver_host = os.environ.get('GEOSERVER_HOST')
print(geoserver_host,"******************")
geoserver_user_path = (os.environ.get('GEOSERVER_USER_PATH'))
print(geoserver_user_path,"******************")

geo = Geoserver(geoserver_host, username='admin', password='geoserver')

def uploadrasterdata(name='default',filename='defailt',extension='ing'):
    try:
        print('UPLOAD-RASTER-DATA',name,filename,extension)
        geo.create_workspace(workspace='demo2')
        geo.create_coveragestore(layer_name=name ,path=f'{settings.BASE_DIR}/media/image/{filename}.{extension}', workspace='demo2')    
    #fix this case!!!
    #what about when same name file are in media/rasterimage/
    #django changes the name automatically
    except Exception as e:
        print(e)    

class RasterImageViewset(viewsets.ModelViewSet):
    queryset=RasterImage.objects.all()
    serializer_class=RasterImageSerializer
    
    def create(self, request, *args, **kwargs):
        try:
            serializer=RasterImageSerializer(data=request.data)
            if serializer.is_valid():
                filename=str(request.data['file'])
                filename=filename.split(".")
                filenameonly=filename[0]
                extension=filename[1]
                serializer.save(filename=filename[0], extension=filename[1])
                
                try: 
                    name=request.POST.get('name')
                    uploadrasterdata(name,filenameonly,extension)
                except Exception as e:
                    return Response(data={"message":str(e)}, status=401)
                
                return Response(data={"message":"Success"}, status=200)
            else:
                return Response(data=serializer.errors, status=400)
        except Exception  as e:
            return Response(status=400,data={"message": str(e)})
    
    def retrieve(self, request, pk=None):
        # id=request.GET.get('id')
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data=serializer.data
        print(data)
        path=geoserver_user_path+'/wms?service=WMS&version=1.1.0&request=GetMap'+'&layers=demo2%3Abtif.tif'+'&bbox=330470.0%2C3054480.0%2C337760.0%2C3064410.0'+'&width=563&height=768'+'&srs=EPSG%3A32645'+'&styles='+'&format=image/png'
        data['path']=path
        return Response(data={"data":data,"message":"successful"},status=200)
        # return Response({"message":id},status=200)

    
    