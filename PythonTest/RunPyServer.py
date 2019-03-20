from itty import *
import requests
#from PythonTest import ApiHelper


def sendSparkGET(url):
    
    #This method is used for:
    #    -retrieving message text, when the webhook is triggered with a message
    #    -Getting the username of the person who posted the message if a command is recognized
    
    header = {
        "Accept" : "application/json",
        "Content-Type":"application/json",
        "Authorization": "Bearer " + accessTokenBot
    }

    response = requests.get(url, headers=header)

    return response

def sendSparkPOST(url, data):
   
    #This method is used for:
    #    -posting a message to the Spark room to confirm that a command was received and processed
   
    header = {
        "Accept" : "application/json",
        "Content-Type":"application/json",
        "Authorization": "Bearer " + accessTokenBot
    }

    response = requests.post(url, json.dumps(data), headers=header)
    
    return response
   

@post('/')
def index(request):
    webhook = json.loads(request.body)
    print (webhook['data']['id'])
    result = sendSparkGET('https://api.ciscospark.com/v1/messages/{0}'.format(webhook['data']['id']))
    result = json.loads(result)
    print (result)

    msg = None
    if webhook['data']['personEmail'] != bot_email:
        if 'batman' in result.get('text', '').lower():
            msg = "I'm Batman!"
        elif 'batcave' in result.get('text', '').lower():
            msg = "The Batcave is silent..."
        elif 'batsignal' in result.get('text', '').lower():
            msg = "NANA NANA NANA NANA"
        if msg != None:
            print (msg)
            sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": msg})

    return "true"



bot_email = "LiveTickerTestBot@webex.bot"
bot_name = "GifSlave9000"
accessTokenBot = "MjM5NTk5YjMtOWEzYS00YWNkLWFkZWEtNTRhZTZlZTEyZmRmNjAxNmNmNGMtZDU1s"
bat_signal  = "https://upload.wikimedia.org/wikipedia/en/c/c6/Bat-signal_1989_film.jpg"

run_itty(server='wsgiref', host='0.0.0.0', port=443)

