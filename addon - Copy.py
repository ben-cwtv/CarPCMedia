import calendar
import datetime
import sys
import os
import xbmc
import xbmcgui
import xbmcaddon
import socket
import threading
import time


###################################################################################################
###################################################################################################
# Initialization
###################################################################################################
###################################################################################################
ACTION_PREVIOUS_MENU = 10
ACTION_SELECT_ITEM = 7

TEXT_ALIGN_LEFT = 0
TEXT_ALIGN_RIGHT = 1
TEXT_ALIGN_CENTER_X = 2
TEXT_ALIGN_CENTER_Y = 4
TEXT_ALIGN_RIGHT_CENTER_Y = 5
TEXT_ALIGN_LEFT_CENTER_X_CENTER_Y = 6


# Get global paths
addon = xbmcaddon.Addon(id = "plugin.program.radioFM")
resourcesPath = os.path.join(addon.getAddonInfo('path'),'resources') + '/'
mediaPath = os.path.join(addon.getAddonInfo('path'),'resources','media') + '/'

addonW = 1280
addonH = 720

# ---------------Buttons Configuration------------------------------
#Lable Frequency
FREQ_LABEL_X        = 50
FREQ_LABEL_Y        = 220
FREQ_LABEL_W        = 450
FREQ_LABEL_H        = 110
FREQ_LABEL_FONT = 'WeatherTemp'

# Home Button
BUTTON_HOME_X = 500
BUTTON_HOME_Y = 200
BUTTON_HOME_W = 83
BUTTON_HOME_H = 83

# Left Seek Button
BUTTON_SEEK_LEFT_X = FREQ_LABEL_X
BUTTON_SEEK_LEFT_Y = FREQ_LABEL_Y + FREQ_LABEL_H
BUTTON_SEEK_LEFT_W = 164
BUTTON_SEEK_LEFT_H = 117

#Store Button (+)
BUTTON_STORE_X = BUTTON_SEEK_LEFT_X + BUTTON_SEEK_LEFT_W
BUTTON_STORE_Y = BUTTON_SEEK_LEFT_Y
BUTTON_STORE_W = 150
BUTTON_STORE_H = 117

#Right Seek Button
BUTTON_SEEK_RIGHT_X = BUTTON_SEEK_LEFT_X + BUTTON_SEEK_LEFT_W + BUTTON_STORE_W
BUTTON_SEEK_RIGHT_Y = BUTTON_SEEK_LEFT_Y
BUTTON_SEEK_RIGHT_W = 164
BUTTON_SEEK_RIGHT_H = 117

#Delete Button
BUTTON_DELETE_X = BUTTON_SEEK_LEFT_X + BUTTON_SEEK_LEFT_W
BUTTON_DELETE_Y = BUTTON_SEEK_LEFT_Y  + BUTTON_SEEK_LEFT_H
BUTTON_DELETE_W = 150
BUTTON_DELETE_H = 117


RADIO_TEXT_X        = 20
RADIO_TEXT_Y        = 640
RADIO_TEXT_W        = 1280
RADIO_TEXT_H        = 100
RADIO_TEXT_FONT = 'font40_title'

STATION_NAME_W        = 300
STATION_NAME_H        = 100
STATION_NAME_X        = addonW - STATION_NAME_W
STATION_NAME_Y        = 15
STATION_NAME_FONT = 'font40_title'

STATION_LIST_X = 545
STATION_LIST_Y = 110
STATION_LIST_W = 275
STATION_LIST_H = 570
STATION_LIST_FONT = 'font30'
STATION_LIST2_X = STATION_LIST_X + STATION_LIST_W + 5
STATION_LIST2_Y = STATION_LIST_Y
STATION_LIST2_W = STATION_LIST_W
STATION_LIST2_H = STATION_LIST_H


# Current Frequency label
currentFreq = xbmcgui.ControlLabel(
        FREQ_LABEL_X, FREQ_LABEL_Y,
        FREQ_LABEL_W, FREQ_LABEL_H,
        'Channel Index',
        textColor='0xffffffff',
        font=FREQ_LABEL_FONT,
        alignment=TEXT_ALIGN_RIGHT)

# List of Preset Stations
stationsList = xbmcgui.ControlList(
        STATION_LIST_X,
        STATION_LIST_Y,
        STATION_LIST_W,
        STATION_LIST_H,
        STATION_LIST_FONT,
        buttonTexture=mediaPath + "middle.png",
        buttonFocusTexture=mediaPath + 'middle_focus.png',
        _itemHeight = 60,
        _alignmentY = -8)

# List 2 of Preset Stations
stationsList2 = xbmcgui.ControlList(
        STATION_LIST2_X,
        STATION_LIST2_Y,
        STATION_LIST2_W,
        STATION_LIST2_H,
        STATION_LIST_FONT,
        buttonTexture=mediaPath + "middle.png",
        buttonFocusTexture=mediaPath + 'middle_focus.png',
        selectedColor = '0x00000000',
        _itemHeight = 60,
        _alignmentY = -8)


# Radio Text label
radioText = xbmcgui.ControlLabel(
        RADIO_TEXT_X, RADIO_TEXT_Y,
        RADIO_TEXT_W, RADIO_TEXT_H,
        addon.getLocalizedString(id=30000),
        textColor='0xffffffff',
        font=RADIO_TEXT_FONT,
        alignment=TEXT_ALIGN_LEFT)

class RadioFM(xbmcgui.WindowDialog):

        def __init__(self):
            #----------------Addon Layout Start----------------------
            # Background
            self.w = addonW
            self.h = addonH
            self.background=xbmcgui.ControlImage(0, 0, self.w, self.h, mediaPath + "black-backround.png")
            self.addControl(self.background)

            #------Start Bottom Right Button Layouts------------------
            #Bottom Right Home Button Border
            self.button_home_background=xbmcgui.ControlImage(self.w - 100, self.h - 93, 83, 83, mediaPath + "button_boarder.png")
            self.addControl(self.button_home_background)
            
            # Home button contained in the above border
            self.button_home=xbmcgui.ControlButton(self.w - 100,
                                                   self.h - 93,
                                                   83,
                                                   83,
                                                   "",
                                                   "icon_home.png",
                                                   "icon_home.png",
                                                   0,
                                                   0)
            self.addControl(self.button_home)
            
            #Bottom Right dab Button Boarder
            self.button_dab_background=xbmcgui.ControlImage(self.w - 184, self.h - 93, 83, 83, mediaPath + "button_boarder.png")
            self.addControl(self.button_dab_background)
            
            # dab button contained in the above border
            self.button_dab=xbmcgui.ControlButton(self.w - 184, self.h - 93, 83, 83, "", "icon_home.png", "icon_home.png", 0, 0)
            self.addControl(self.button_dab)           
                        
            #Bottom Right fm Button Boarder
            self.button_fm_background=xbmcgui.ControlImage(self.w - 268, self.h - 93, 83, 83, mediaPath + "button_boarder.png")
            self.addControl(self.button_fm_background)

            # fm button contained in the above border
            self.button_fm=xbmcgui.ControlButton(self.w - 268, self.h - 93, 83, 83, "", "icon_home.png", "icon_home.png", 0, 0)
            self.addControl(self.button_fm)
            #------End Bottom Right Button Layouts------------------
            
            #------Start Station List Layout------------------------
            #Station List Lable
            self.station_lable_header=xbmcgui.ControlLabel(55,177,400,400,'Station List',textColor='0xffffffff',font='font36_title',alignment=0)
            self.addControl(self.station_lable_header)
   
            #Station List border
            self.button_surroundstationlist_background=xbmcgui.ControlImage(17, 173, 1247, 550, mediaPath + "listborder.png")
            self.addControl(self.button_surroundstationlist_background)        
            
            #------End Station List Layout--------------------------
            

            #----------------Addon Layout Finish---------------------

            '''
            
            # text background
            self.addControl(currentFreq)

            # Add Labels
            self.addControl(radioText)








            # Left button
            self.button_left=xbmcgui.ControlButton(BUTTON_SEEK_LEFT_X,
                                                                                            BUTTON_SEEK_LEFT_Y,
                                                                                            BUTTON_SEEK_LEFT_W,
                                                                                            BUTTON_SEEK_LEFT_H,
                                                                                            "",
                                                                                            mediaPath + "prev_focus.png",
                                                                                            mediaPath + "prev.png")
            self.addControl(self.button_left)
            self.setFocus(self.button_left)

            # Right button
            self.button_right=xbmcgui.ControlButton(BUTTON_SEEK_RIGHT_X,
                                                                                            BUTTON_SEEK_RIGHT_Y,
                                                                                            BUTTON_SEEK_RIGHT_W,
                                                                                            BUTTON_SEEK_RIGHT_H,
                                                                                            "",
                                                                                            mediaPath + "next_focus.png",
                                                                                            mediaPath + "next.png")
            self.addControl(self.button_right)
            self.setFocus(self.button_right)

            # Store Station Button
            self.button_store=xbmcgui.ControlButton(BUTTON_STORE_X,
                                                                                            BUTTON_STORE_Y,
                                                                                            BUTTON_STORE_W,
                                                                                            BUTTON_STORE_H,
                                                                                            "",
                                                                                            mediaPath + "settings_focus.png",
                                                                                            mediaPath + "settings.png",
                                                                                            0,
                                                                                            0,
                                                                                            alignment=TEXT_ALIGN_CENTER_X)
            self.addControl(self.button_store)
            self.setFocus(self.button_store)

            #Delete Button
            self.button_delete=xbmcgui.ControlButton(BUTTON_DELETE_X,
                                                                                            BUTTON_DELETE_Y,
                                                                                            BUTTON_DELETE_W,
                                                                                            BUTTON_DELETE_H,
                                                                                            "",
                                                                                            mediaPath + "delete_focus.png",
                                                                                            mediaPath + "delete.png",
                                                                                            0,
                                                                                            0,
                                                                                            alignment=TEXT_ALIGN_CENTER_X)

            self.addControl(self.button_delete)
            self.setFocus(self.button_delete)





'''


            # Store original window ID
            self.prevWindowId = xbmcgui.getCurrentWindowId()



# Start the Addon
dialog = RadioFM()
dialog.doModal()
del dialog