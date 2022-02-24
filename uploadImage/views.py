from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required

import cv2
import base64
import numpy as np
class UploadImage(APIView):
    def encode_img(self,location):
        im=cv2.imread(r'C:\Users\duvvu\Downloads\Nikhil\Centennial\Sem_4\SoftwareDev\picsketcher\picsketcher-main\uploadImage\Assets\HappyFace.jpg')
        im_resize=cv2.resize(im,(500,500))
        image_bytes = cv2.imencode('.jpg', im_resize)[1].tobytes()
    
        return image_bytes
    def decode_image(self,img_bytes):
        try:
            # CV2
            nparr = np.fromstring(img_bytes, np.uint8)
            img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR) # cv2.IMREAD_COLOR in OpenCV 3.1
        except:
            return Response('error in decoding the bytes image')

        
        return img_np


    def render_image(self,image):
        try:
            img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            img_blur = cv2.GaussianBlur(img_gray, (21,21), 0, 0)
            img_blend = cv2.divide(img_gray, img_blur, scale=256)
        except:
            return Response('Error in image filtering')
        return img_blend
    # @login_required
    def post(self, request):
        # if request.user.is_authenticated:
        #     print("yessssssss")
        # else:
        #     print("Noooooooooooo")
        bytes_text = self.encode_img('./Assets/HappyFace.jpg') #replace this method with the bytes data from front end request
        # response = request.data
        # bytes_text = response['img']
        #convert string to image
        image_s= self.decode_image(bytes_text)
        
        image_filtered = self.render_image(image_s)
        cv2.imwrite('test.jpg',image_filtered)
        return Response(image_filtered)
