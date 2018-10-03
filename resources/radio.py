from keystone.radio import Radio

radio_board = "/dev/ttyACM0"

def dab():
    #Check if the device is ready to receive commands
    try:
        with Radio("/dev/ttyACM0", 0, 0) as r:
            status = r.is_system_ready()    
        except:
            return "False"
        
    return status

    #Call with self.playDAB(Mode, Index)
def playDAB(self, mode, index):
    with Radio(radio_board, mode, index) as r:

        r.get_total_program

        program = r.programs
        r.volume = 11
        r.stereo = True
        program.play

        time_lable = pyxbmct.Label(program.name, alignment=pyxbmct.ALIGN_CENTER, font='header50_title')
        self.placeControl(time_lable, 3, 2, 2, 2)
            
def nextDAB(self, mode, index):
     with Radio(radio_board, mode, index) as r:
	       r.get_total_program

        program = r.programs
        r.volume = 11
        r.stereo = True
        #program.play
        r.nextstream
        time_lable = pyxbmct.Label(program.name, alignment=pyxbmct.ALIGN_CENTER, font='header50_title')
        self.placeControl(time_lable, 3, 2, 2, 2)
