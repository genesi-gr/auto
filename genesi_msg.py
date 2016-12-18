# -*- coding: utf-8 -*-                                                                                                                                                                  
from websocket_messaging import websocket_send

class car(object):

    def __init__( self , carName ):
        self.carName = carName
        self.socket_server = 'http://genesi.gr:1234'
        self.pwd = input('Κωδικός ')

    def carSend( self , msg ):
        websocket_send( self.socket_server , msg , self.pwd , self.carName )

    def nxw( self ):
        self.carSend( 'ηχώ' )

    def prosw( self , taxutnta=50. ):
        self.carSend( 'πρόσω%3d'%taxutnta )

    def anapoda( self , taxutnta=50. ):
        self.carSend( 'ανάποδα%3d'%taxutnta )

    def aristera( self ):
        self.carSend( 'αριστερά' )

    def deksia( self ):
        self.carSend( 'δεξιά' )

    def vekra( self ):
        self.carSend( 'νεκρά' )

    def diakopn( self ):
        self.carSend( 'διακοπή' )
