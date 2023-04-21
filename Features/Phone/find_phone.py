from twilio.rest import Client
from Body.Speaker import Speak


# Use https://www.twilio.com/en-us for sid & token

def find_phone():
    account_sid = ''
    auth_token = ''
    client = Client(account_sid, auth_token)
    message = client.calls.create(
        twiml='<Response><Say>Found Your Phone Sir!!, If this Phone does not belong to You then call on '
              '9011022124..</Say></Response>',
        call_reason='Found Your Phone Sir!!, If this Phone does not belong to You then call on 9011022124..',
        from_='Phone Number You Got From https://www.twilio.com/en-us',
        to='Your Number',
        url="https://demo.twilio.com/docs/voice.xml")
    Speak("Finding your phone Sir , it will take four to five seconds !!!")


