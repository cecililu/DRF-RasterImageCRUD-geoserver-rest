from django.shortcuts import render
from rest_framework import viewsets
from geo.Geoserver import Geoserver
from django.conf import settings
from core.models import RasterImage
from rest_framework.response import Response
from api.serializers.serializers import RasterImageSerializer
import os

geoserver_host = os.environ.get('GEOSERVER_HOST')
geoserver_user_path = (os.environ.get('GEOSERVER_USER_PATH'))
geo = Geoserver(geoserver_host, username='admin', password='geoserver')

def uploadrasterdata(name,filename,extension):
    """
    this function makes request to the geoserver to
    CREATE WORKSPACE and add raster layer 
    """
    try:
        print('UPLOAD-RASTER-DATA',name,filename,extension)
        geo.create_workspace(workspace='demo2')
        geo.create_coveragestore(layer_name=name ,path=f'{settings.BASE_DIR}/media/image/{filename}.{extension}', workspace='demo2')    
        #fix this case!!!
        #what about when same name file are in media/rasterimage/
        #django changes the name automatically
    except Exception as e:
        print(e) 

def deleteraster(name):
    """
    deletes the raster data in geoserver
    """
    print("deleting raster---->",name)
    try:
        geo.delete_layer(layer_name=name, workspace='demo2')
    except Exception as e:
        print(e)
def updateraster(name):
    """
    deletes the raster data in geoserver
    """
    try:
        geo.delete_layer(layer_name=name, workspace='demo2')
    except Exception as e:
        print(e)



class RasterImageViewset(viewsets.ModelViewSet):
    queryset=RasterImage.objects.all()
    serializer_class=RasterImageSerializer
    
    def create(self, request, *args, **kwargs):
        """
        adds file name and extension automatically to the model instance by reading from user request
        """
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
                
                return Response(data={"message":"success"}, status=200)
            else:
                return Response(data=serializer.errors, status=400)
        except Exception  as e:
            return Response(status=400,data={"message": str(e)})
    
    def destroy(self,request,*args,**kwargs):        
        try:
            instance = self.get_object() 
            self.perform_destroy(instance)
            deleteraster(instance.name)
            return Response(status=200,data={"message":"Raster data delete successfully"})
        except Exception as e:
            return Response(status=400,data={"message":str(e)})
    
    def retrieve(self, request, pk=None):  
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        name=serializer.data['name']
        data=serializer.data
        # path=geoserver_user_path+'/wms?service=WMS&version=1.1.0&request=GetMap'+'&layers=demo2%3A'+str(name)+'&width=563&height=768'+'&srs=EPSG%3A32645'+'&styles='+'&format=image/png'
        data['wmsurl']=geoserver_user_path
        data['version']="1.1.0"
        data['layername']="demo2:"+name
        data['EPSG']="EPSG:4326"
        return Response(data={"data":data,"message":"success"},status=200)
    
    def update(self, request, *args, **kwargs):
        partial=kwargs.pop('partial',False)
        instance = self.get_object()
        serializer=RasterImageSerializer(instance,data=request.data,partial=partial)
        if serializer.is_valid():
                filename=str(request.data['file'])
                name=request.POST.get('name')
                filename=filename.split(".")
                filenameonly=filename[0]
                extension=filename[1]
                deleteraster(instance.name)
                self.perform_update(serializer)
                uploadrasterdata(name,filenameonly,extension)
                return Response(data={"message":"Success","data":serializer.data},status=200)
        else:
                return Response(status=400,data={"message":serializer.errors})
       
                





    
    