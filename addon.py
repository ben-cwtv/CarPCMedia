import os
import xbmc
import xbmcaddon
import pyxbmct
import resources.radio as radio

_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')


mode = 0index = 0

# Enable or disable Estuary-based design explicitly
# pyxbmct.skin.estuary = True

class MyAddon(pyxbmct.AddonDialogWindow):

    def __init__(self, title=''):
        super(MyAddon, self).__init__(title)
        self.setGeometry(1280, 720, 8, 6)
        self.set_base_layout()
    	   self.checkboard()
        # Connect a key action (Backspace) to close the window.
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
        

    def set_base_layout(self):
        #Time Lable
        time_label = pyxbmct.Label(xbmc.getInfoLabel('system.time'), alignment=pyxbmct.ALIGN_CENTER, font='header50_title')
        self.placeControl(time_label, 0, 0, 1, 2)
        
        self.volume_button = pyxbmct.Button('Volume', alignment=pyxbmct.ALIGN_CENTER, font='button34_title')
        self.placeControl(self.volume_button, 0, 4, pad_x=0, pad_y=5)
        
        self.home_button = pyxbmct.Button('Home', alignment=pyxbmct.ALIGN_CENTER, font='button34_title')
        self.placeControl(self.home_button, 0, 5, pad_x=0, pad_y=5)
        
        self.radio_button = pyxbmct.Button('Radio', alignment=pyxbmct.ALIGN_CENTER, font='button34_title')
        self.placeControl(self.radio_button, 1, 0, pad_x=0, pad_y=5)
        self.connect(self.radio_button, self.radio)
        
        self.mp3_button = pyxbmct.Button('Mp3', alignment=pyxbmct.ALIGN_CENTER, font='button34_title')
        self.placeControl(self.mp3_button, 1, 1, pad_x=0, pad_y=5)
        
        self.bluetooth_button = pyxbmct.Button('Bluetooth', alignment=pyxbmct.ALIGN_CENTER, font='button34_title')
        self.placeControl(self.bluetooth_button, 1, 2, pad_x=0, pad_y=5)
        
        self.aux_button = pyxbmct.Button('AUX', alignment=pyxbmct.ALIGN_CENTER, font='button34_title')
        self.placeControl(self.aux_button, 1, 3, pad_x=0, pad_y=5)
        
        self.spotify_button = pyxbmct.Button('Spotify', alignment=pyxbmct.ALIGN_CENTER, font='button34_title')
        self.placeControl(self.spotify_button, 1, 4, pad_x=0, pad_y=5)
        
        self.spare_button = pyxbmct.Button('Spare', alignment=pyxbmct.ALIGN_CENTER, font='button34_title')
        self.placeControl(self.spare_button, 1, 5, pad_x=0, pad_y=5)
        
    def radio(self):
        self.prev_button = pyxbmct.Button('Prev', alignment=pyxbmct.ALIGN_CENTER, font='button34_title')
        self.placeControl(self.prev_button, 4, 1)
        
        freq_type_lable = pyxbmct.Label('FM', alignment=pyxbmct.ALIGN_CENTER, font='header34_title')
        self.placeControl(freq_type_lable, 4, 4, 1, 1)
        
        self.next_button = pyxbmct.Button('Next', alignment=pyxbmct.ALIGN_CENTER, font='button34_title')
        self.placeControl(self.next_button, 4, 5)
        self.connect(self.next_button, lambda: dab.nextDAB(0,0))
        
        # List
        self.station_fm_list = pyxbmct.List(font='font30_title', _itemHeight=40)
        #self.list(Row Location (Where pos) , column Location (where Pos) , No Items, text Span over column no)
        self.placeControl(self.station_fm_list, 2, 0, 10, 1)
        # Add items to the list
        items = ['Items {0}'.format(i) for i in range(1, 11)]
        self.station_fm_list.addItems(items)
        
        # Connect the list to a function to display which list item is selected.
        self.connect(self.station_fm_list, lambda: xbmc.executebuiltin('Notification(Note!,{0} selected.)'.format(
        self.station_fm_list.getListItem(self.station_fm_list.getSelectedPosition()).getLabel())))
        
        self.mw_button = pyxbmct.Button('MW', alignment=pyxbmct.ALIGN_CENTER, font='button34_title')
        self.placeControl(self.mw_button, 7, 3)
        
        self.fm_button = pyxbmct.Button('FM', alignment=pyxbmct.ALIGN_CENTER, font='button34_title')
        self.placeControl(self.fm_button, 7, 4)
        
        self.dab_button = pyxbmct.Button('DAB', alignment=pyxbmct.ALIGN_CENTER, font='button34_title')
        self.placeControl(self.dab_button, 7, 5)
        #self.connect(self.dab_button, self.playDAB(0,0))
        
    def checkboard(self):
	       result = radio.dab()
        if result == True:
            radioboard = pyxbmct.Label('True' , alignment=pyxbmct.ALIGN_CENTER, font='header50_title')
            self.placeControl(radioboard, 0, 3, 1, 0)
        else:
            radioboard = pyxbmct.Label('False' , alignment=pyxbmct.ALIGN_CENTER, font='header50_title')
            self.placeControl(radioboard, 0, 3, 1, 0)

        

if __name__ == '__main__':
    window = MyAddon('Audio Addon')
    window.doModal()
    # Destroy the instance explicitly because
    # underlying xbmcgui classes are not garbage-collected on exit.
    del window