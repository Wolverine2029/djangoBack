import datetime

from django.shortcuts import render, redirect
from .models import RegisteredUsers, UnRegisteredUsers, tickets
# Create your views here.
from django.shortcuts import render
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)
import cv2
import glob


# firebase = firebase.FirebaseApplication("https://eyeconic-c6280-default-rtdb.firebaseio.com/", None)
# data = {
#     'Name': 'Naveen',
#     'Email': 'aniljobs506@gmail.com',
#     'License': 'NAV123'
# }
# result = firebase.post("/eyeconic-c6280-default-rtdb/UnegisteredUsers", data)
# print(result)

import firebase_admin as fa
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate("/Users/anilkumar/Downloads/eyeconic/main/drone/firebasekey.json")
fa.initialize_app(cred)

data = {'name': 'Sunny', 'email': 'munnacinqstar@gmail.com', 'license' : 'SUN123'}
# db.collection('UnregUsers').add(data)

def Users_List(request, license):
    # logger.info('Requested users list ' + str(datetime.datetime.now()) + ' hours!')
    #
    # db = firestore.client()
    # docs = db.collection('RegUsers').where("license", "==", license).get()
    # print("gg ******",docs)
    # for doc in docs:
    #     print(doc.to_dict())
    # docs1 = db.collection('UnregUsers').where("license", "==", license).get()
    #
    # for doc in docs1:
    #     print(doc.to_dict())
    # from firebase import firebase
    # from firebase_admin import db
    # firebase = firebase.FirebaseApplication("https://eyeconic-c6280-default-rtdb.firebaseio.com/", None)
    # reg = firebase.get('/eyeconic-c6280-default-rtdb/RegisteredUsers', '')
    # print(reg)
    # ru = db.reference("RegisteredUsers").get()
    # for user in ru.each():
    #     print(user.val())
    # unreg = firebase.get('/eyeconic-c6280-default-rtdb/UnegisteredUsers', '')
    # print(unreg)

    i, n = checkImage()
    print("Fianl image: ", i)
    print("Fianl plate number: ", n)
    users = RegisteredUsers.objects.all()
    unReg = UnRegisteredUsers.objects.all()
    issueTicket = True
    licenseNum = license
    checklicense = ''
    print(licenseNum)
    message = "Car is not registed with UMKC. Issue Ticket?"
    for usr in users:
        logger.info('Entered for loop registered users')
        if usr.license == licenseNum:
            logger.info('Entered If condition')
            message = "Car is registered at UMKC"
            issueTicket = False
            checklicense = 'yes'
        else:
            for unreg in unReg:
                logger.info('Entered unregistered users loop')
                if unreg.license == licenseNum:
                    logger.info('Entered unregistered users loop IF condition')
                    message = "Car is Unregistered. Issue Ticket?"
                    checklicense = 'no'

    print(message)
    context = {
        'users': users,
        'unreg': unReg,
        'message' : message,
        'issueTicket' : issueTicket,
    }
    print(checklicense)
    img = 'YBP75307'
    return render(request, 'drone/list.html' ,context)

def issueTicket(request):
    licenseNum = request.POST.get("license")
    ticks = tickets.objects.all()
    for i in ticks:
        if i == licenseNum:
            message = "Ticket Already Issued."
    new_ticket = tickets(license=request.POST.get('license'))
    new_ticket.save()
    context = {
        'message': "Issued Ticket Successfully",
    }
    logger.warning('Issuing Ticket to : ' + str(licenseNum))
    return render(request, 'drone/list.html' ,context)

def checkImage():

    # file = '/Users/anilkumar/Downloads/eyeconic/main/drone/images/'+ str(img) + '.jpg'
    # image = cv2.imread(file)
    # print(type(image))
    # cv2.imshow(image)
    # return image
    lenOfFile = 0

        # for line in lines:
        #     print("lines: ", line)
    lenOfFile = 0
    import time
    waitFlag = True
    timeout = time.time() + 60*10 # Wait 10 minutes
    timeout_start = time.time()
    image = 0
    number = ''
    initialcheck = 0 # Dummy
    with open('/Users/anilkumar/Downloads/eyeconic/main/drone/images/output.txt') as f:
        if f.readlines == "\n": lenOfFile = 0
        else: lenOfFile = len(f.readlines())

        print("Length of file in first check: ", lenOfFile)
    while waitFlag == True:
        print("Sleeping 1 min for license plate")
        time.sleep(10)  # waits 10s
        with open('/Users/anilkumar/Downloads/eyeconic/main/drone/images/output.txt') as f:
            if f.readlines == "\n": lenOfFile1 = 0
            else: lenOfFile1 = len(f.readlines())
            print("Length of file read in the latest check: ", lenOfFile1)
            initialcheck = lenOfFile1 # Dummy
        if (lenOfFile1 > lenOfFile) & (time.time() < timeout_start + timeout):
            print("Data found in output.txt")
            with open('/Users/anilkumar/Downloads/eyeconic/main/drone/images/output.txt') as f:
                lines = f.readlines()[-1]
                print("New License Plate Number:", lines)
                number = lines
                print(lines, "   gggg")
            waitFlag = False

    img = '/Users/anilkumar/Downloads/eyeconic/main/drone/images/'+ str(number) + '.jpg'
    image = cv2.imread(img)
    print(type(image))
    return lines, image
    # import glob
    # import os
    # list_of_files = glob.glob('/Users/anilkumar/Downloads/eyeconic/main/drone/images/*.jpg')  # * means all if need specific format then *.csv
    # latest_file = max(list_of_files, key=os.path.getctime)
    # print(latest_file)


def check_user(request):
    if 'license' in request.POST:
        pass
    # do somethings
    users = RegisteredUsers.objects.all()
    context = {
        'users': users,
    }

    return render(request, context)


def create_user(request):
    return render(request, 'drone/create.html', context)


def delete_user(request, pk):
    return render(request, 'drone/delete.html', context)


def edit_user(request, pk):
    return render(request, 'drone/update.html', context)
