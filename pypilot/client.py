#!/usr/bin/env python
#
#   Copyright (C) 2020 Sean D'Epagnier
#
# This Program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.  

from __future__ import print_function

import socket, select, sys, os, time
import heapq
import pyjson
from bufferedsocket import LineBufferedNonBlockingSocket
from values import Value

DEFAULT_PORT = 23322

try:
    IOError
except:
    class IOError(Exception):
        pass
try:
    ourPOLLNVAL = select.POLLNVAL
except:
    print('select.POLLNVAL not defined, using 32')
    ourPOLLNVAL = 32
    
class ConnectionLost(Exception):
    pass

class Watch(object):
    def __init__(self, value, period):
        self.value = value
        self.period = period
        self.time = time.monotonic()

class ClientWatch(Value):
    def __init__(self, values, client):
        super(ClientWatch, self).__init__('watch', {})
        self.values = values
        self.client = client

    def set(self, values):
        for name in values:
            value = self.values[name]
            period = values[name]
            if period is False:
                value.watch = False
            else:
                if period is True:
                    period = 0
                value.watch = Watch(value, period)
                value.pwatch = True
                
                self.client.send(name + '=' + value.get_msg() + '\n') # initial send

class ClientValues(Value):
    def __init__(self, client):
        self.value = False
        super(ClientValues, self).__init__('values', False)
        self.client = client
        self.values = {'values': self}
        self.values['watch'] = ClientWatch(self.values, client)
        self.wvalues = {}
        self.pqwatches = []

    def set(self, values):
        if type(self.value) == type(False):
            self.value = values
        else:
            for name in values:
                self.value[name] = values[name]

    def send_watches(self):
        t0 = time.monotonic()
        while self.pqwatches:
            if t0 < self.pqwatches[0][0]:
                break # no more are ready
            t, i, watch = heapq.heappop(self.pqwatches) # pop first element
            self.client.send(watch.value.name + '=' + watch.value.get_msg() + '\n')
            watch.time = t0+watch.period
            watch.value.pwatch = True # can watch again once updated
            
    def insert_watch(self, watch):
        heapq.heappush(self.pqwatches, (watch.time, time.monotonic(), watch))

    def register(self, value):
        if value.name in self.values:
            print('warning, registering existing value:', value.name)
        self.wvalues[value.name] = value.info
        self.values[value.name] = value

    def get_msg(self):
        ret = pyjson.dumps(self.wvalues)
        self.wvalues = {}
        return ret

class pypilotClient(object):
    def __init__(self, host=False):        
        self.values = ClientValues(self)
        self.watches = {}
        self.wwatches = {}
        self.received = []

        if host and type(host) != type(''):
            # host is the server object
            self.server = host
            self.connection = host.pipe()
            self.poller = select.poll()
            fd = self.connection.fileno()
            if fd:
                self.poller.register(fd, select.POLLIN)
            return

        config = {}
        try:
            configfilepath = os.getenv('HOME') + '/.pypilot/'
            if not os.path.exists(configfilepath):
                os.makedirs(configfilepath)
            if not os.path.isdir(configfilepath):
                raise configfilepath + 'should be a directory'
        except Exception as e:
            print('os not supported')
            configfilepath = '/.pypilot/'
        self.configfilename = configfilepath + 'pypilot_client.conf'

        try:
            file = open(self.configfilename)
            config = pyjson.loads(file.readline())
            file.close()
                
        except Exception as e:
            print('failed to read config file:', self.configfilename, e)
            config = {}

        if host:
            if ':' in host:
                i = host.index(':')
                config['host'] = host[:i]
                config['port'] = host[i+1:]
            else:
                config['host'] = host
        if not 'host' in config:
            config['host'] = '127.0.0.1'

        if not 'port' in config:
            config['port'] = DEFAULT_PORT
        self.config = config
            
        self.connection = False # connect later

    def onconnected(self, connection):
        # write config if connection succeeds
        try:
            file = open(self.configfilename, 'w')
            file.write(pyjson.dumps(self.config) + '\n')
            file.close()
            self.write_config = False
        except IOError:
            print('failed to write config file:', self.configfilename)
        except Exception as e:
            print('Exception writing config file:', self.configfilename, e)
        
        self.connection = LineBufferedNonBlockingSocket(connection)
        self.poller = select.poll()
        self.poller.register(self.connection.socket, select.POLLIN)
        self.wwatches = self.watches
        for name in self.values.values:
            if name != 'values' and name != 'watch':
                self.values.wvalues[name] = self.values.values[name].info

    def poll(self, timeout=0):
        if not self.connection:
            if not self.connect(False):
                return
            
        # inform server of any watches we have
        if self.wwatches:
            self.connection.send('watch=' + pyjson.dumps(self.wwatches) + '\n')
            self.wwatches = {}

        # send any delayed watched values
        self.values.send_watches()

        # flush output
        self.connection.flush()

        if self.connection.fileno():
            try:
                events = self.poller.poll(int(1000 * timeout))
            except Exception as e:
                print('exception polling', e)
                self.disconnected()
                return

            if not events:
                return # no data ready
            
            fd, flag = events.pop()
            if flag & select.POLLIN:
                if self.connection and not self.connection.recv():
                    self.disconnected() # recv returns 0 means connection closed
                    return
            else: # other flags indicate disconnect
                self.disconnected()

        # read incoming data line by line
        while True:
            t0 = time.monotonic()
            line = self.connection.readline()
            if not line:
                return
            try:
                name, data = line.rstrip().split('=', 1)
                if name == 'error':
                    print('server error', data)
                    continue
                value = pyjson.loads(data)
            except Exception as e:
                print('invalid message from server:', line)
                print('reason', e)
                raise Exception

            if name in self.values.values:
                self.values.values[name].set(value)
            else:
                self.received.append((name, value))
                

    # polls at least as long as timeout
    def disconnected(self):
        self.connection.close()
        raise ConnectionLost

    def connect(self, verbose=True):
        try:
            host_port = self.config['host'], self.config['port']
            connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connection.settimeout(3)
            connection.connect(host_port)
        except Exception as e:
            if verbose:
                print('connect failed to %s:%d' % host_port)
                print('reason', e)
            return False

        self.onconnected(connection)
        return True
    
    def receive_single(self):
        if self.received:
            ret = self.received[0]
            self.received = self.received[1:]
            return ret
        return False

    def receive(self, timeout=0):
        self.poll(timeout)
        ret = {}
        for msg in self.received:
            name, value = msg
            ret[name] = value
        self.received = []
        return ret

    def send(self, msg):
        if self.connection:
            self.connection.send(msg)
    
    def set(self, name, value):
        # quote strings
        if type(value) == type('') or type(value) == type(u''):
            value = '"' + value + '"'
        elif type(value) == type(True):
            value = 'true' if value else 'false'
        self.send(name + '=' + str(value) + '\n')

    def watch(self, name, value=True):
        self.watches[name] = value
        self.wwatches[name] = value

    def register(self, value):
        self.values.register(value)
        value.client = self
        return value

    def list_values(self, timeout=10):
        t0 = time.monotonic()
        self.watch('values')
        while True:
            self.poll(timeout)
            if type(self.values.value) != type(False):
                return self.values.value
        return False

    def info(self, name):
        return self.values.value[name]

def pypilotClientFromArgs(args, period=True):
    host = False
    if len(args) > 1:
        host = args[1]

    client = pypilotClient(host)
    if not client.connect(False):
        if host:
            client = pypilotClient()
            watches = args[1:]
            client.connect()
        if not client.connection:
            print('failed to connect')
            exit(1)

    # set any value specified with path=value
    for arg in args[2:]:
        if '=' in arg:
            self.send(arg + '\n')
            arg, value = line.rstrip().split('=', 1)
        watches.append(arg)

    # args without = are watched
    for name in watches:
        client.watch(name, period)
    return client
    
# this simple test client for an autopilot server
# connects, enumerates the values, and then requests
# each value, printing them
def main():
    import signal
    def quit(sign, frame):
        exit(0)
    signal.signal(signal.SIGINT, quit)

    if '-h' in sys.argv:
        print('usage', sys.argv[0], '[host] -i -c -h [NAME[=VALUE]]...')
        print('eg:', sys.argv[0], '-i imu.compass')
        print('   ', sys.argv[0], 'servo.max_slew_speed=10')
        print('-i', 'print info about each value type')
        print('-c', 'continuous watch')
        print('-h', 'show this message')
        exit(0)

    args = list(sys.argv)
    continuous = '-c' in args
    if continuous:
        args.remove('-c')

    info = '-i' in args
    if info:
        args.remove('-i')
        
    period = True if continuous else 100 # 100 second period to just get the value once
    client = pypilotClientFromArgs(args, period)
    if not client.watches: # retrieve all values
        watches = client.list_values()
        for name in watches:
            client.watch(name, period)

    if not continuous:
        values = {}
        t0 = time.monotonic()
        while len(values) < len(client.watches):
            dt = time.monotonic() - t0
            if dt > 10:
                print('timeout retrieving values')
                exit(1)
                    
            client.poll(.1)
            msgs = client.receive()
            for name in msgs:
                values[name] = msgs[name]

            
        names = sorted(values)
        for name in names:
            if info:
                print(name, client.info(name), '=', values[name])
            else:
                maxlen = 76
                result = name + ' = ' + str(values[name])
                if len(result) > maxlen:
                    result = result[:maxlen] + ' ...'
                print(result)
    else:
        while True:
            client.poll(1)
            msg = client.receive_single()
            if msg:
                name, data = msg
                if info:
                    print(name, client.info(name), '=', data)
                else:
                    print(name, '=', data)

if __name__ == '__main__':
    main()