from django.shortcuts import render,redirect
import pyrebase
from django.contrib import messages,auth

import requests
import json

URL = 'https://www.sms4india.com/api/v1/sendCampaign'



config={
    'apiKey': "AIzaSyCzrLaRxqdVHSMA8ytUv3BMwD9Jjcmyl54",
    'authDomain': "messageapp-e9500.firebaseapp.com",
    'databaseURL': "https://messageapp-e9500.firebaseio.com",
    'projectId': "messageapp-e9500",
    'storageBucket': "messageapp-e9500.appspot.com",
    'messagingSenderId': "280684575834",
    
}

firebase = pyrebase.initialize_app(config)

authr  = firebase.auth()

database= firebase.database()

def signup(request):
    if request.method == 'POST':
        if 'login' in request.POST:
            name = request.POST.get('name')
            email = request.POST.get('email')    
            password = request.POST.get('password')

            try:
                user = authr.sign_in_with_email_and_password(email,password)
                return render(request,'message.html',{'username':name})
            except:
                message="Invalid Credentials"
                return render(request,'index.html',{'message':message})


        if request.method == 'POST':
            if 'signup' in request.POST:
                name = request.POST.get('name')
                email = request.POST.get('email')    
                password = request.POST.get('password')

                try:
                    user = authr.create_user_with_email_and_password(email,password)

                    uid = user['localId']

                    data={'name':name,'status':"1"}


                    database.child('users').child(uid).child('details').set(data)

                    signsuccess="SignIn Successful"
                    return render(request,"index.html",{'signsuccess':signsuccess})        

                except:
                    signinerror="SignIn Error. Please try again!!"
                    return render(request,'index.html',{'signinerror':signinerror})

    return render(request,'index.html')


def logout(request):
    auth.logout(request);
    return redirect('/')    

def send_message(request):
    if request.method=='POST':
        number=request.POST.get('number')
        message=request.POST.get('message')
        m= f'message'
        print(number)
        print(message)
        try:    
            response = sendPostRequest(URL, 'VW28D2NFBQ9E39H1QGFMGZK06LSR26IW', 'WVPIBGSG9389BS6Z', 'stage', '8097020354', 'tanmayjadhavtj11@gmail.com', )
            print(response.text)
        except:
            message.info('Not Sent')
    return render(request,'message.html') 

def sendPostRequest(reqUrl, apiKey, secretKey, useType, phoneNo, senderId, textMessage):
    req_params = {
    'apikey':apiKey,
    'secret':secretKey,
    'usetype':useType,
    'phone': phoneNo,
    'message':textMessage,
    'senderid':senderId
    }
    return requests.post(reqUrl, req_params)
