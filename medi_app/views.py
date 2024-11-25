import requests
import json

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from medi_app.credentials import LipanaMpesaPpassword, MpesaAccessToken
# Import the model
from .models import Appointment
# Import the login_required
from django.contrib.auth.decorators import login_required


@login_required
# Create your views here.
def home(request):
    """ Display the home page """
    return render(request, 'index.html')

def about(request):
    """ Display the about page """
    return render(request, 'about.html')

@login_required(login_url='accounts:login')
def appointment(request):
    """ Appointment booking """
    # Check if its a post method
    if request.method == 'POST':
        # Create variable to pick the input fields
        appointments = Appointment(
            # list the input fields here
            name = request.POST['name'],
            email = request.POST['email'],
            phone = request.POST['phone'],
            date = request.POST['date'],
            department = request.POST['department'],
            doctor = request.POST['doctor'],
            message = request.POST['message'],
        )
        # save the variable
        appointments.save()
        # redirect to a page
        return redirect('medi_app:home')
    else:
        return render(request, 'appointment.html')


# Retrieve all appointments
def retrieve_appointments(request):
    """ Retrieve/fetch all appointments """
    # Create a variable to store these appointments
    appointments = Appointment.objects.all()
    context = {
        'appointments':appointments
        }
    return render(request, 'show_appointments.html', context)


# Delete
def delete_appointment(request, id):
    """ Deleting """
    appointment = Appointment.objects.get(id=id) # fetch the particular appointment by its ID
    appointment.delete() # actual action of deleting
    return redirect("medi_app:show_appointments") # just remain on the same page


# Update
def update_appointment(request, appointment_id):
    """ Update the appointments """
    appointment = get_object_or_404(Appointment, id=appointment_id)
    # Put the condition for the form to update
    if request.method == 'POST':
        appointment.name = request.POST.get('name')
        appointment.email = request.POST.get('email')
        appointment.phone = request.POST.get('phone')
        appointment.date = request.POST.get('date')
        appointment.doctor = request.POST.get('doctor')
        appointment.department = request.POST.get('department')
        appointment.message = request.POST.get('message')
        # Once you click on the update button
        appointment.save()

        return redirect("medi_app:show_appointments")
    
    context = {'appointment': appointment}
    return render(request, "update_appointment.html", context)




# Adding the mpesa functions

#Display the payment form
def pay(request):
   """ Renders the form to pay """
   return render(request, 'pay.html')


# Generate the ID of the transaction
def token(request):
    """ Generates the ID of the transaction """
    consumer_key = 'qvQFfRUmIIMKcLutXyGEdAbkKtYN7RzIjVKiMz8Ma94qQt4q'
    consumer_secret = 'HRSVAAGk1AEG4ZATjzWmqYSTpGluFG6Erf8gRab85NEepozIGSmTPmR6k2Cu9Ivr'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token":validated_mpesa_access_token})


# Send the stk push
def stk(request):
    """ Sends the stk push prompt """
    if request.method =="POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "eMobilis",
            "TransactionDesc": "Web Development Charges"
        }
        response = requests.post(api_url, json=request, headers=headers)
        return HttpResponse("Success")