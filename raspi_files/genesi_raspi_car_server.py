# -*- coding: utf-8 -*-
import sys
import os
import websocket
import hmac
import urllib
import urllib.request

try:
    import RPi.GPIO as GPIO
    on_ras = True
except ImportError:
    on_ras = False 

def websocket_send(url, message, hmac_key=None, group='default'):
    sig = hmac_key.encode() and hmac.new(hmac_key.encode(), message.encode()).hexdigest() or ''
    params = urllib.parse.urlencode(
        {'message': message, 'signature': sig, 'group': group})
    f = urllib.request.urlopen(url, params.encode())
    data = f.read()
    f.close()
    return data

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
                print('Setting up pin %d'%pin, flush=True)
                GPIO.setup( pin , GPIO.OUT )
                GPIO.PWM( pin , freq )
                p_pwm.append( GPIO.PWM( pin , freq ) )
                p_pwm[-1].start( 100 )
            self.p_pwm = p_pwm
            for pin in self.binary_pin:
                print('Setting up pin %d'%pin, flush=True)
                GPIO.setup( pin , GPIO.OUT )
                GPIO.output( pin , True )
                

    def prosw( self , taxutnta=100. ):
        taxutnta = 100. - taxutnta
        if on_ras:
            taxutnta = max( taxutnta , 0. )
            taxutnta = min( taxutnta , 50. )
            self.p_pwm[1].ChangeDutyCycle( 100. )
            self.p_pwm[0].ChangeDutyCycle( taxutnta )

    def anapoda( self , taxutnta=100. ):
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

diakomistns = 'genesi.gr:1234/'
diaulos     = 'genesi.gr:1234/realtime/'

car = auto()

def on_msg( ws , msg ):

    print('Μήνυμα:', msg, flush=True)
    if 'ηχώ' in msg:
        print('ηχώ', flush=True)
        websocket_send('http://' + diakomistns , msg , pwd , 'ηχώ')
    elif 'νεκρά' in msg:
        print('Νεκρά', flush=True)
        car.vekra()
    elif 'διακοπή' in msg:
        os.system( 'sudo poweroff' )
    else:
        if 'πρόσω' in msg:
            taxutnta = int( msg[-3:] )
            print('Πρόσω', flush=True)
            car.prosw( taxutnta )
        elif 'ανάποδα' in msg:
            taxutnta = int( msg[-3:] )
            print('Ανάποδα', flush=True)
            car.anapoda( taxutnta )
        if 'αριστερά' in msg:
            print('Αριστερά', flush=True)
            car.aristera()
        elif 'δεξιά' in msg:
            print('Δεξιά', flush=True)
            car.deksia()

def onError( self , error_msg ):
    print(error_msg, file=sys.stderr, flush=True)

if __name__ == '__main__':

    omada = sys.argv[1]
    ws = websocket.WebSocketApp('ws://' + diaulos + omada , on_message=on_msg)
    print('Συνδέθηκε η ομάδα', omada)
    ws.run_forever()

