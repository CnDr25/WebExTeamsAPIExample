import requests
import json
import sys

class ApiHelper:

    accessToken = ""
    urlStart = "https://api.ciscospark.com/v1/"
    noRoomFoundError = False


    def __init__(self, accessToken_p):
        self.accessToken = accessToken_p



    def setMessageToSpark(self, roomName, msg, isGifBot):
        urlEnd = "messages"

        roomID = self.getRoomID(roomName)

        if not(self.noRoomFoundError):
            if not(isGifBot):
                payload = "{\"roomId\": \"" + roomID + "\",\"markdown\": \"" + msg + "\"}"
            else:
                print("Message to GifBot will be prepared")
                self.isGifBotInRoom(roomID)
                payload = "{\"roomId\": \"" + roomID + "\",\"markdown\": \"<@personEmail:gifbot@webex.bot|GifMaster9000> " + msg + "\"}"

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

        roomID = response['id']  

        return roomID



    def addMemberToRoom(self, roomName, memberMail, isRoomName):
        if (isRoomName):
            roomID = self.getRoomID(roomName)
        else:
            self.noRoomFoundError = False
            roomID = roomName
        
        if not(self.noRoomFoundError):
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

        roomFound = False

        for item in response["items"]:
            if(item['title'] == roomName):
                roomID = item['id']   
                roomFound = True

        if(roomFound):
            self.noRoomFoundError = False
            return roomID
        else:
            self.noRoomFoundError = True
            tempText = "No Room with the Name \"" + roomName + "\" was found"
            print(tempText)
            return "No_Room_was_found"



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

roomName = "Test_Bereich_von_API"

apiHelper.setMessageToSpark(roomName, "hello", True)

apiHelper.setMessageToSpark(roomName, "This Gif was send by Python", False)