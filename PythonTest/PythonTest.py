import requests
import json
import sys

class ApiHelper:

    accessToken = ""
    urlStart = "https://api.ciscospark.com/v1/"

    def __init__(self, accessToken_p):
        self.accessToken = accessToken_p



    def setMessageToSpark(self, roomName, msg, isGifBot):
        urlEnd = "messages"

        roomID = self.getRoomID(roomName)

        if not(isGifBot):
            payload = "{\"roomId\": \"" + roomID + "\",\"markdown\": \"" + msg + "\"}"
        else:
            print("Message to GifBot will be prepared")
            self.isGifBotInRoom(roomID)
            payload = "{\"roomId\": \"" + roomID + "\",\"markdown\": \"<@personEmail:gifbot@webex.bot|GifBot> " + msg + "\"}"

        headers = {
            'Content-Type': "application/json",
            'Authorization': "Bearer " + self.accessToken,
        }

        response = requests.request("POST", self.urlStart + urlEnd , data=payload, headers=headers)



    def createNewRoom(self, title):
        urlEnd = "rooms"

        payload = "{\"title\": \"" + title + "\"}"

        headers = {
            'Content-Type': "application/json",
            'Authorization': "Bearer " + self.accessToken,
        }

        response = requests.request("POST", self.urlStart + urlEnd , data=payload, headers=headers).json()

        print(response)

        return roomID



    def addMemberToRoom(self, roomName, memberMail, isRoomName):
        if (isRoomName):
            roomID = self.getRoomID(roomName)
        else:
            roomID = roomName
        
        urlEnd = "memberships"

        payload = "{\"roomId\": \"" + roomID + "\",\"personEmail\": \"" + memberMail + "\"}"

        headers = {
            'Content-Type': "application/json",
            'Authorization': "Bearer " + self.accessToken,
        }

        response = requests.request("POST", self.urlStart + urlEnd , data=payload, headers=headers)
        print("Member added")



    def getRoomID(self, roomName):
        urlEnd = "rooms"

        headers = {
            'Authorization': "Bearer " + self.accessToken,
        }

        response = requests.get(self.urlStart + urlEnd , headers=headers).json()

        for item in response["items"]:
            if(item['title'] == roomName):
                roomID = item['id']   
    
        return roomID



    def isGifBotInRoom(self, roomID):

        gifBotMail = "gifbot@webex.bot"
        
        urlEnd = "memberships"

        paraQuery = {"roomId": roomID}

        headers = {
            'Content-Type': "application/json",
            'Authorization': "Bearer " + self.accessToken,
        }
        
        response = requests.request("GET", self.urlStart + urlEnd , params=paraQuery, headers=headers).json()

        inRoom = False

        for item in response["items"]:
            if (item['personEmail'] == gifBotMail):
                print("GifBot is in room")
                inRoom = True   
        
        if not (inRoom):
            print("GifBot is not in room but will be added")
            self.addMemberToRoom(roomID, gifBotMail, False)



#Put Access Token here
apiHelper = ApiHelper("ACCESSTOKEN")

roomName = "Test-Space-New"

apiHelper.setMessageToSpark(roomName, "hello", True)

apiHelper.setMessageToSpark(roomName, "This Gif was send by Python", False)






#class TestClass:
#    def __init__(self):
#        pass
#    def writeText(self, text1, text2):
#        print(text1)
#        sleep(2)
#        print(text2) 
##------------------------------------
#tc = TestClass()
#tc.writeText("Hello", "World")

