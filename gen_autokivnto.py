try:
    import RPi.GPIO as GPIO
    on_ras = True
except ImportError:
    on_ras = False 

class auto( object ):

    def __init__( self ):
        if on_ras:
            prosw_pin = 12
            anapoda_pin = 16
            aristera_pin = 20
            deksia_pin = 21
            self.pwm_pin = [ prosw_pin , anapoda_pin ]
            self.binary_pin = [ aristera_pin , deksia_pin ]
            freq = 100000
            GPIO.setmode( GPIO.BCM )
            p_pwm = []
            for pin in self.pwm_pin:
                print 'Setting up pin %d'%pin
                GPIO.setup( pin , GPIO.OUT )
                GPIO.PWM( pin , freq )
                p_pwm.append( GPIO.PWM( pin , freq ) )
                p_pwm[-1].start( 100 )
            self.p_pwm = p_pwm
            for pin in self.binary_pin:
                print 'Setting up pin %d'%pin
                GPIO.setup( pin , GPIO.OUT )
                GPIO.output( pin , True )
                

    def prosw( self , taxutnta=50. ):
        taxutnta = 100. - taxutnta
        if on_ras:
            taxutnta = max( taxutnta , 0. )
            taxutnta = min( taxutnta , 50. )
            self.p_pwm[1].ChangeDutyCycle( 100. )
            self.p_pwm[0].ChangeDutyCycle( taxutnta )

    def anapoda( self , taxutnta=50. ):
        taxutnta = 100. - taxutnta
        if on_ras:
            taxutnta = max( taxutnta , 0. )
            taxutnta = min( taxutnta , 50. )
            self.p_pwm[0].ChangeDutyCycle( 100. )
            self.p_pwm[1].ChangeDutyCycle( taxutnta )
        pass

    def deksia( self ):
        if on_ras:
            GPIO.output( self.binary_pin[0] , False )
            GPIO.output( self.binary_pin[1] , True )

    def aristera( self ):
        if on_ras:
            GPIO.output( self.binary_pin[0] , True )
            GPIO.output( self.binary_pin[1] , False )

    def isia( self ):
        if on_ras:
            GPIO.output( self.binary_pin[0] , True )
            GPIO.output( self.binary_pin[1] , True )

    def vekra( self ):
        if on_ras:
            for p in self.p_pwm:
                p.ChangeDutyCycle( 100. )
            for pin in self.binary_pin:
                GPIO.output( pin , True )
