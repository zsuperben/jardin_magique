class DocHandler(APIHandler):

    def get():
        helper = '''
        This is a short doc to the API :
        Used URLS are :             (r'/measure/', MeasureHandler, dict(Conf=Conf)),
            (r'/switch/(?P<swurl>SW\d)/', SwitchHandler), => Directly controls switches on the PCB. Low Level, Should work both with the parameter supplied as uri..
            (r'/switch/', SwitchHandler), => This is the same controler using JSON DATA PUT OR DELETE ONLY 
            (r'/video/', VideoHandler),  => GET ONLY : return picture taken by the camera
            (r'/arrosage/', ArrosageHandler), => WATER SEEDS PUT AND GET 
            (r'/tomates/', TomatesHandler), =>  WATER TOMATOES PUT AND GET 
            (r'/remplir/', RemplissageHandler), FILLS UP WATER TANK FOR SEEDS : PUT AND GET 
            (r'/carrottes/', CarrottesHandler), WASTES WATER ON THE GROUND FOR NO PURPUSE.. XD 

        '''
        self.write(helper)
