from twilio.rest import Client
from Body.Speaker import Speak


def find_phone():
    account_sid = 'AC5691066a967bb3dbd4a0b920d537ef53'
    auth_token = '292df4acaf38ff4252b29e8eb722bb41'
    client = Client(account_sid, auth_token)
    message = client.calls.create(
        twiml='<Response><Say>Found Your Phone Sir!!, If this Phone does not belong to You then call on '
              '9011022124..</Say></Response>',
        call_reason='Found Your Phone Sir!!, If this Phone does not belong to You then call on 9011022124..',
        from_='+1 218 395 5886',
        to='+91 9604304414',
        url="https://demo.twilio.com/docs/voice.xml")
    Speak("Finding your phone Sir , it will take four to five seconds !!!")


