import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import RegisteredUsers, UnRegisteredUsers, tickets
# Create your views here.
from django.shortcuts import render
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)
import cv2
import glob
import smtplib, ssl
from email.message import EmailMessage


# firebase = firebase.FirebaseApplication("https://eyeconic-c6280-default-rtdb.firebaseio.com/", None)
# data = {
#     'Name': 'Naveen',
#     'Email': 'aniljobs506@gmail.com',
#     'License': 'NAV123'
# }
# result = firebase.post("/eyeconic-c6280-default-rtdb/UnegisteredUsers", data)
# print(result)

# import firebase_admin as fa
# from firebase_admin import credentials
# from firebase_admin import firestore
# cred = credentials.Certificate("/Users/anilkumar/Downloads/eyeconic/main/drone/firebasekey.json")
# fa.initialize_app(cred)

data = {'name': 'Sunny', 'email': 'munnacinqstar@gmail.com', 'license' : 'SUN123'}
# db.collection('UnregUsers').add(data)

def Users_List(license):
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

    # i, n = checkImage()
    # print("Fianl image: ", i)
    # print("Fianl plate number: ", n)
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
    return checklicense

def issueTicket(request, license):
    licenseNum = license
    issued = ''
    ticks = tickets.objects.all()
    for i in ticks:
        if i == licenseNum:
            issued = 'no'
        else:
            new_ticket = tickets(license=request.POST.get('license'))
            new_ticket.save()
            print("Issued ticket Successfully")
            issued = 'yes'
            break
    print("Issuing complete")
    logger.warning('Issuing Ticket to : ' + str(licenseNum))
    return HttpResponse(issued)

def email_service(license):
    unReg = UnRegisteredUsers.objects.all()
    sentStatus = ''
    ln = license
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "munnacinqstar@gmail.com"  # Enter your address
    receiver_email = ''  # Enter receiver address
    message = EmailMessage()
    message['Subject'] = 'Issued Ticket to car - ' + str(ln) + ' at UMKC parking area.'
    message['From'] = 'anilkumarkochera@gmail.com'
    message['To'] = 'akkw32@umsystem.edu'
    for unreg in unReg:
        logger.info('Entered unregistered users loop')
        if unreg.license == ln:
            logger.info('Entered unregistered users loop IF condition')
            receiver_email = str(unreg.email)
            message['To'] = str(unreg.email)
            print("Sending ticket email to: ", receiver_email)
    # Create the plain-text and HTML version of your message
    text = """\
    Hi,
    Due to your unauthorized parking at UMKC campus, Ticket has been issued to your automobile."""
    html = """\
    <html>
      <body>
        <p>Hi,<br>
           Acknowledge this mail by paying your ticket.<br>
        </p>
      </body>
    </html>

    """

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, 'Smartass@2025')
            server.sendmail(sender_email, receiver_email, message)
            sentStatus = 'yes'
    except Exception as e:
        print("An error occured while sending email", e)
        sentStatus = 'no'
    return HttpResponse(sentStatus)

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
                number = lines
                print("License Platae Number: ", lines)
            waitFlag = False

    # img = '/Users/anilkumar/Downloads/eyeconic/main/drone/images/'+ str(number) + '.jpg'
    # image = cv2.imread(img)
    # print(type(image))
    user_status = Users_List(lines)
    emailstatus = email_service(lines)
    return HttpResponse({'userValidation': user_status, 'license': lines, 'email': emailstatus})
    # import glob
    # import os
    # list_of_files = glob.glob('/Users/anilkumar/Downloads/eyeconic/main/drone/images/*.jpg')  # * means all if need specific format then *.csv
    # latest_file = max(list_of_files, key=os.path.getctime)
    # print(latest_file)
