# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ImageStorage
import cv2
import base64
import numpy as np
class UploadImage(APIView):
    def encode_img(self,location):
        try:
            # print(type(location))
            im=cv2.imread(location)
            im_resize=cv2.resize(im,(500,500))
            image_bytes = cv2.imencode('.jpg', im_resize)
            jpg_as_text = base64.b64encode(image_bytes[1])
        except:
            return Response({"success":False,"message":"error in encoding image"})    
        return jpg_as_text
    def decode_image(self,img_base_64):
        try:
            # CV2
            jpg_original = base64.b64decode(img_base_64)
            jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
            image_buffer = cv2.imdecode(jpg_as_np, flags=1)
        except:
            return Response({"success":False,"message":"error in decoding the bytes image"})

        
        return image_buffer


    def render_image(self,image):
        try:
            img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            img_blur = cv2.GaussianBlur(img_gray, (21,21), 0, 0)
            img_blend = cv2.divide(img_gray, img_blur, scale=256)
        except:
            return Response({"success":False,"message":"Error in image filtering"})
        return img_blend
    def post(self, request):
        #encoding image uploaded to base64
        bytes_text = request.data["image_bytes"] #replace this method with the bytes data from front end request
        #decoding to np array
        image_s= self.decode_image(bytes_text)
        # #applying filters
        image_filtered = self.render_image(image_s)
        #encoding filtered image
        image_bytes = cv2.imencode('.jpg', image_filtered)
        jpg_as_text = base64.b64encode(image_bytes[1])
        # cv2.imwrite('Assets/test.jpg',image_filtered)
        return Response({"success":True,"image_bytes":jpg_as_text})
