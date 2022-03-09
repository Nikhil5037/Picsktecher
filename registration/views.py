from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RegisteredUsers
import jwt, datetime
import re   
class Index(APIView):
    def post(self,request):
        return Response({"Success":True})

# Create your views here.
class Register(APIView):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    message=''
    def checkEmail(self,email): 
        if(re.search(self.regex,email)): 
            return False
        else:
            return True 
    def password_check(self,passwd):
        SpecialSym =['$', '@', '#', '%']
        val = False
        if len(passwd) < 8:
            val=True
            self.message='length should be at least 8'
            return val
            
        if len(passwd) > 20:
            val = True
            self.message='length should be not be greater than 20'
            return val
        if not any(char.isdigit() for char in passwd): 
            val = True
            self.message='Password should have at least one numeral'
            return val
        if not any(char.isupper() for char in passwd):
            val = True
            self.message  ='Password should have at least one uppercase letter'
            return val
        if not any(char.islower() for char in passwd):
            val = True
            self.message = 'Password should have at least one lowercase letter'
            return val
        if not any(char in SpecialSym for char in passwd):
            val = True
            self.message = 'Password should have at least one of the symbols $@#'
            return val
        if val:
            return val

    
    def post(self, request):
        field_names = sorted(
            [field.name for field in RegisteredUsers._meta.get_fields()])
        print(field_names)
        request_keys = sorted(request.data.keys())
        print(request_keys)
        field_names.remove("id")

        if request_keys != field_names:
            return Response("Some fields are missing.", status=status.HTTP_400_BAD_REQUEST)
        email = request.data["email"]
        password = request.data["password"]
        firstname = request.data["firstname"]
        lastname = request.data["lastname"]
        if self.checkEmail(email):
            return Response({"success":False,"message":"Unable to register---Invalid Email Format"})
        if not((firstname.isalpha()) and (lastname.isalpha())):
            return Response({"success":False,"message":"Unable to register---First and Last Name should be alphabetical"})
        if self.password_check(password):
            return Response({"success":False,"message":"incorrect password format--"+self.message})

        try:
            user = RegisteredUsers.objects.create(
            email=email,
            password=password,
            firstname=firstname,
            lastname=lastname
        )
            user.save()
        except:
            return Response({"success":False,"message":"Please enter a unique email"})

        return Response({"success":True,"message":"user successfully registered"})


class Login(APIView):
       
    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]
        try:
            user = RegisteredUsers.objects.get(email=email)
            if user.password == password:
                payload={
                    'id': user.id,
                    'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                    'iat':datetime.datetime.utcnow()

                }
                token = jwt.encode(payload,'secret',algorithm='HS256')
                response=Response()
                response.set_cookie(key='jwt',value=token,httponly=True)
                response.data= {"success":True, "message":"Successfully logged in",'jwt':token}
            
                return response
        except:
            return Response({"success":False,"message":"User with the given email does not exist"})
class UserView(APIView):
    def get(self,request):
        token= request.COOKIES.get('jwt')
        if not token:
            return Response({"message":"unauthentiated"})
        try:
            payload =jwt.decode(token,'secret',algorithms = ["HS256"])
        except:
            return Response({"message":"unauthentiated"})
        user = RegisteredUsers.objects.filter(id=payload['id']).first()
        return Response({"success":True,"user":user.email})
               