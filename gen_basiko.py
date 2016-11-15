# -*- coding: utf-8 -*-
import sys
import os
# from twisted.internet import reactor
# from autobahn.twisted.websocket import WebSocketClientFactory, WebSocketClientProtocol, connectWS
from websocket_messaging import websocket_send
import websocket
from gen_autokivnto import auto
# from to_programma_mou import oi_evtoles_mou

diakomistns = 'genesi.gr:1234/'
diaulos     = 'genesi.gr:1234/realtime/'
# pwd         = 'ΚΩΔΙΚΟΣ ΓΙΑ ΤΟΝ ΔΙΑΚΟΜΙΣΤΗ'

car = auto()

def on_msg( ws , msg ):

    print 'Μήνυμα: ' , msg
    if 'ηχώ' in msg:
        print 'ηχώ'
        websocket_send( 'http://' + diakomistns , msg , pwd , 'ηχώ' )
    elif 'νεκρά' in msg:
        print 'Νεκρά'
        car.vekra()
    elif 'διακοπή' in msg:
        os.system( 'poweroff' )
    else:
        if 'πρόσω' in msg:
            taxutnta = int( msg[-3:] )
            print 'Πρόσω'
            car.prosw( taxutnta )
        elif 'ανάποδα' in msg:
            taxutnta = int( msg[-3:] )
            print 'Ανάποδα'
            car.anapoda( taxutnta )
        if 'αριστερά' in msg:
            print 'Αριστερά'
            car.aristera()
        elif 'δεξιά' in msg:
            print 'Δεξιά'
            car.deksia()

def onError( self , error_msg ):
    print error_msg

if __name__ == '__main__':

    omada = sys.argv[1]
    ws = websocket.WebSocketApp( 'ws://' + diaulos + omada , on_message=on_msg )
    print 'Συνδέθηκε η ομάδα ' + omada
    ws.run_forever()
    # factory = WebSocketClientFactory( 'ws://' + path_to_server + omada )
    # factory.protocol = EchoClientProtocol
    # connectWS(factory)
    # reactor.run()
