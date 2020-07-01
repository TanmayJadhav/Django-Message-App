from django.shortcuts import render,redirect
import pyrebase
from django.contrib import messages,auth

import requests
import json

URL = 'https://www.sms4india.com/api/v1/sendCampaign'



# Add you firebase Config file here

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
        try:    
            # enter your details from way2sms api 
            response = sendPostRequest(URL, 'provided-api-key', 'provided-secret', 'prod/stage', 'valid-to-mobile', 'active-sender-id', 'message-text' )
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
