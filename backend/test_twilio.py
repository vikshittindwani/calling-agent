from twilio.rest import Client
import os

# Twilio credentials (better: load from .env)
account_sid = "******************************"
auth_token = "***************************"
twilio_number = "************"   # trial number from Twilio
to_number = "+91************"      # tumhara verified number

client = Client(account_sid, auth_token)

call = client.calls.create(
    twiml='<Response><Say voice="alice">Hello! this is my ai voice , thank you.</Say></Response>',
    to=to_number,
    from_=twilio_number
)

print("Call initiated! SID:", call.sid)
