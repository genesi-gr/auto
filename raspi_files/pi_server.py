# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web
import wifi
import subprocess

class MainHandler(tornado.web.RequestHandler):

    def _create_form(self):
        # ssids = ['ses{x}_{x}'.format(x=x) for x in range(10)]
        print('checking networks')
        interface_name = subprocess.check_output('iwconfig', stderr=None).decode().split('\n')[0].split(' ')[0]
        ssids = set([r.ssid for r in wifi.Cell.all(interface_name) if r.ssid != ''])
        print('done')
        html = '<table><th>SSID</th><th>Κωδικός</th><th></th>'
        for i_ssid, ssid in enumerate(ssids):
            html += '''
                <tr>
                    <form method='post'>
                        <td>{ssid}</th>
                        <td>
                            <input type='text' name='password_{ssid}'/>
                        </td>
                        <td>
                            <button>Καταχώρηση</button>
                        </td>
                    </form>
                </tr>
                '''.format(i_ssid=i_ssid, ssid=ssid)
        html += '</table>'
        html += '''
            <form method='post'>
                <button name='wifi' value='wifi'>WiFi</button>
            </form>
            <form method='post'>
                <button name='adhoc' value='adhoc'>AdHoc</button>
            </form>
            <form method='post'>
                <button name='restart' value='restart'>Επανεκκίνηση</button>
            </form>
            <form method='post'>
                <button name='poweroff' value='poweoff'>Τερματισμός</button>
            </form>
        '''
        return html 
    
    def _edit_wpa_file(self, new_network, new_passphrase):
        # file_path = 'wpa_supplicant.conf'
        file_path = '/etc/wpa_supplicant/wpa_supplicant.conf'
        wpa_conf = subprocess.check_output(['sudo', 'cat', file_path]).decode()
        new_wpa_conf = wpa_conf.split('network')[0]
        for settings in wpa_conf.split('network')[1:]:
            if new_network not in settings:
                new_wpa_conf += 'network' + settings
        wpa_new_settings = subprocess.check_output(['wpa_passphrase', new_network, new_passphrase]).decode()
        new_wpa_conf += '\n' + wpa_new_settings
        subprocess.os.system('echo \'{}\' | sudo tee {} > /dev/null'.format(new_wpa_conf, file_path))

    def get(self):
        self.write(self._create_form())

    def post(self):
        print('clicked?')
        for key in self.request.arguments:
            if 'password' in key:
                ssid = key.split('_')[1]
                pswd = self.request.arguments[key][0]
                print(ssid, pswd)
                self._edit_wpa_file(ssid, pswd)
            elif 'restart' in key:
                subprocess.os.system('sudo shutdown -r now')
            elif 'poweroff' in key:
                subprocess.os.system('sudo shutdown -h now')
            elif 'wifi' in key:
                subprocess.call(['sudo', 'cp', '/etc/network/interfaces-wifi', '/etc/network/interfaces'])
            elif 'adhoc' in key:
                subprocess.call(['sudo', 'cp', '/etc/network/interfaces-adhoc', '/etc/network/interfaces'])

        self.write(self._create_form())

def make_app():
    return tornado.web.Application([
        (r'/', MainHandler),
    ])

if __name__ == '__main__':
    app = make_app()
    app.listen(8000, address='0.0.0.0')
    tornado.ioloop.IOLoop.current().start()
import os
import subprocess

