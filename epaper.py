from struct import pack
from enum import Enum


class Colors(Enum):
    BLACK = pack('B', 0)
    DARK_GRAY = pack('B', 1)
    LIGHT_GRAY = pack('B', 2)
    WHITE = pack('B', 3)

class FontSize(Enum):
    SMALL = pack('B', 0)
    MEDIUM = pack('B', 1)
    BIG = pack('B', 2)

class Epaper():

    def __init__(self, port='/dev/ttyAMA0', baudrate=115200, debug=False):
        if not debug:
            import serial
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(11, GPIO.OUT)
            GPIO.setup(13, GPIO.OUT)
            GPIO.output(11, GPIO.HIGH)
            GPIO.output(13, GPIO.LOW)
            self.__serial = serial.Serial(port=port, baudrate=rate)
        else:
            class s():
                def write(content):
                    print(content)
            self.__serial = s

        assert self.__prepare_message(b'\x00') == b'\xA5\x00\x09\x00\xCC\x33\xC3\x3C\xAC'

        self.__serial.write(self.__prepare_message(b'\x00'))


    def __convert_int(self, num):
        retval = b''
        low = num
        high = 0
        while low > 255:
            high = high + 1
            low = low - 256

        return pack('B', high) + pack('B', low)


    def __get_coords(self, x, y):
        assert x <= 800
        assert y <= 600
        return self.__convert_int(x) + self.__convert_int(y)


    # message length + checksum
    def __prepare_message(self, body):
        x = 0
        length = pack('B', len(body) + 6 + 2)
        body = b'\xA5\x00' + length + body + b'\xCC\x33\xC3\x3C'
        for b in body:
            x = x ^ b
        return body + pack('B', x)


    def clear(self):
        self.__serial.write(self.__prepare_message(b'\x2E'))


    def refresh(self):
        self.__serial.write(self.__prepare_message(b'\x0A'))


    def text(self, x, y, text):
        body = b''
        for c in text:
            body += pack('B', ord(c))
        body = b'\x30' + self.__get_coords(x, y) + body + b'\x00'
        self.__serial.write(self.__prepare_message(body))


    def set_font_size(self, size):
        body = b'\x1E' + size
        self.__serial.write(self.__prepare_message(body))


    def point(self, x, y):
        body = b'\x20' + self.__get_coords(x, y)
        self.__serial.write(self.__prepare_message(body))


    def line(self, x1, y1, x2, y2):
        body = b'\x22' + self.__get_coords(x1, y1) + self.__get_coords(x2, y2)
        self.__serial.write(self.__prepare_message(body))


    def rectangle(self, x1, y1, x2, y2, fill=True):
        if fill:
            body = b'\x24' + self.__get_coords(x1, y1) + self.__get_coords(x2, y2)
        else:
            body = b'\x25' + self.__get_coords(x1, y1) + self.__get_coords(x2, y2)
        self.__serial.write(self.__prepare_message(body))


    def circle(self, x, y, r, fill=True):
        if fill:
            body = b'\x27' + self.__get_coords(x1, y1) + self.__convert_int(r)
        else:
            body = b'\x26' + self.__get_coords(x1, y1) + self.__convert_int(r)
        self.__serial.write(self.__prepare_message(body))


    def triangle(self, x1, y1, x2, y2, x3, y3, fill=True):
        if fill:
            body = b'\x29' + self.__get_coords(x1, y1) + self.__get_coords(x2, y2) + self.__get_coords(x3, y3)
        else:
            body = b'\x28' + self.__get_coords(x1, y1) + self.__get_coords(x2, y2) + self.__get_coords(x3, y3)
        self.__serial.write(self.__prepare_message(body))


