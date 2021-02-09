# -*- coding: utf-8 -*-
from websocket_messaging import websocket_send

class car(object):

    def __init__(self, car_name):
        """Διαθέσιμες εντολές:
        prosw()
        anapoda()
        aristera()
        deksia()
        vekra()
        """
        self.car_name = car_name
        self._socket_server = 'http://genesi.gr:1234'
        self._pwd = input('Κωδικός ')

    def _car_send(self, msg):
        websocket_send(self._socket_server, msg, self._pwd, self.car_name)

    def nxw(self):
        self._car_send('ηχώ')

    def prosw(self, taxutnta=50.):
        self._car_send('πρόσω%3d'%taxutnta)

    def anapoda(self, taxutnta=50.):
        self._car_send('ανάποδα%3d'%taxutnta)

    def aristera(self):
        self._car_send('αριστερά')

    def deksia(self):
        self._car_send('δεξιά')

    def vekra(self):
        self._car_send('νεκρά')

    def diakopn(self):
        answer = input('Είσαι σίγουρος ότι θες να σβήσεις το αυτοκινητάκι;[ναι/όχι]').lower()
        if answer in ['nai', 'vai', 'yes', 'y']:
            self._car_send('διακοπή')
