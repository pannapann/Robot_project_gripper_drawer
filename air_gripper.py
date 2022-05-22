import serial
import time
import math
from gpiozero import LED

# Define gripper and its pin on Raspberry Pi
GRIPPER_PIN = 3
gripper = LED(GRIPPER_PIN)

class IAI_Robot:
    def __init__(self, set_port, set_baudrate, set_timeout):
        """
        Initialize the robot object and set it back to home position.
        """
        
        # Initiate serial connection
        self.ser = serial.Serial(set_port, set_baudrate, timeout=set_timeout)

        # Turn on xyz servo
        self.ser.write('!00232071b0\r\n'.encode())
        read = self.ser.readline().decode()
        print(read + '\n')
        time.sleep(1)

        # Go back to home position
        self.home()
    
    def home(self):
        """
        Go to the home position (0, 0, 0)
        """
        self.ser.write('!0023307000000a0\r\n'.encode())
        read = self.ser.readline().decode()
        print(read + '\n')
        time.sleep(6)
        
    def move(self, message_id, axis, acceleration, speed, x_target, y_target, z_target):
        """
        Move robot to the destination coordinates with the specified speed and acceleration.
        """

        if message_id == 'absolute':
            message_id = '234'
        elif message_id == 'relative':
            message_id = '235'

        axis_pattern = 0b0
        if 'x' in axis:
            axis_pattern = axis_pattern + 0b1
        if 'y' in axis:
            axis_pattern = axis_pattern + 0b10
        if 'z' in axis:
            axis_pattern = axis_pattern + 0b100
        byte_format = 2
        byte_adding = byte_format - len(hex(axis_pattern).lstrip('0x'))
        adding_text = ''
        for i in range(0, byte_adding):
            adding_text = adding_text + '0'
        axis_pattern = adding_text + hex(axis_pattern).lstrip('0x')

        byte_format = 4
        byte_adding = byte_format - len(hex(int(acceleration * 100)).lstrip('0x'))
        adding_text = ''
        for i in range(0, byte_adding):
            adding_text = adding_text + '0'
        acceleration = adding_text + hex(int(acceleration * 100)).lstrip('0x')

        byte_format = 4
        byte_adding = byte_format - len(hex(int(speed)).lstrip('0x'))
        adding_text = ''
        for i in range(0, byte_adding):
            adding_text = adding_text + '0'
        speed = adding_text + hex(int(speed)).lstrip('0x')

        position = ''
        byte_format = 8
        if 'x' in axis:
            if x_target >= 0:
                byte_adding = byte_format - len(hex(int(x_target * 1000)).lstrip('0x'))
                adding_text = ''
                for i in range(0, byte_adding):
                    adding_text = adding_text + '0'
                position = position + adding_text + hex(int(x_target * 1000)).lstrip('0x')
            else:
                x_target = -x_target
                position = position + hex(int(16 ** byte_format - x_target * 1000)).lstrip('0x')
        if 'y' in axis:
            if y_target >= 0:
                byte_adding = byte_format - len(hex(int(y_target * 1000)).lstrip('0x'))
                adding_text = ''
                for i in range(0, byte_adding):
                    adding_text = adding_text + '0'
                position = position + adding_text + hex(int(y_target * 1000)).lstrip('0x')
            else:
                y_target = -y_target
                position = position + hex(int(16 ** byte_format - y_target * 1000)).lstrip('0x')
        if 'z' in axis:
            if z_target >= 0:
                byte_adding = byte_format - len(hex(int(z_target * 1000)).lstrip('0x'))
                adding_text = ''
                for i in range(0, byte_adding):
                    adding_text = adding_text + '0'
                position = position + adding_text + hex(int(z_target * 1000)).lstrip('0x')
            else:
                z_target = -z_target
                position = position + hex(int(16 ** byte_format - z_target * 1000)).lstrip('0x')

        string_command = '!00' + message_id + axis_pattern + acceleration + acceleration + speed + position

        checksum = 0
        for i in range(0, len(string_command)):
            checksum = checksum + ord(string_command[i])
        checksum = hex(int(checksum)).lstrip('0x')
        checksum = checksum[len(checksum) - 2:len(checksum)]

        string_command = string_command + checksum

        self.ser.write((string_command + '\r\n').encode())
        read = self.ser.readline().decode()
        print(read + '\n')


    def grab_pen(self):
        """
        Move to pen position and turn on the gripper to grab the pen.
        """
        self.move('absolute','xyz',0.3,100,200,0,100)
        time.sleep(3)
        gripper.on()
        time.sleep(1)
        self.move('absolute','xyz',0.3,100,80,0,0)
        time.sleep(2)
        
    def return_pen(self):
        """
        Move to pen position and turn off the gripper to return the pen.
        """
        time.sleep(2)
        self.move('absolute','xyz',0.3,100,200,0,0)
        time.sleep(4)
        self.move('absolute','z',0.3,100,200,0,100)
        time.sleep(2)
        gripper.off()
        time.sleep(1)
        self.move('absolute','xyz',0.3,100,0,0,0)
        time.sleep(2)
    
    def square(self, x,y,z,size):
        """
        Draw a square with the center position of (x,y,z) and the specified size of each side.
        """
        
        self.grab_pen()
        
        self.move('absolute','xyz',0.3,100,(x-(size*5)),(y+(size*5)),z)
        time.sleep(2)
        self.move('absolute','xyz',0.3,100,(x+(size*5)),(y+(size*5)),z)
        time.sleep(2)
        self.move('absolute','xyz',0.3,100,(x+(size*5)),(y-(size*5)),z)
        time.sleep(2)
        self.move('absolute','xyz',0.3,100,(x-(size*5)),(y-(size*5)),z)
        time.sleep(2)
        self.move('absolute','xyz',0.3,100,(x-(size*5)),(y+(size*5)),z)
        
        self.return_pen()
        
    def circle(self,x,y,z,r=1):
        """
        Draw a circle with the center position of (x,y,z) and the specified size of each side.
        """
        
        self.grab_pen()
        time.sleep(2)
        
        for i in range(180):
            xr=x+r+math.cos(i*2)
            yr=y+r+math.sin(i*2)
            self.move('absolute','xyz',0.3,100,xr,yr,z)
            time.sleep(0.5)
    
        self.return_pen()
        
    def triangle(self,x,y,z,size=1):
        """
        Draw a triangular with the center position of (x,y,z) and the specified size of radius.
        """
        
        self.grab_pen()
        
        time.sleep(2)
        b = size*10
        h = math.sqrt(b**2-(b**2)/4)
        
        self.move('absolute','xyz',0.3,100,(x-h/2),(y+b/2),z)
        time.sleep(2)
        self.move('absolute','xyz',0.3,100,(x+h/2),(y),z)
        time.sleep(2)
        self.move('absolute','xyz',0.3,100,(x-h/2),(y-b/2),z)
        time.sleep(2)
        self.move('absolute','xyz',0.3,100,(x-h/2),(y+b/2),z)
        time.sleep(2)
        
        self.return_pen()

if __name__ == "__main__":
    # IAI settings 
    # Set 'set_port' to /dev/ttyUSB[01] for Raspberry Pi
    set_port = '/dev/ttyUSB0'
    set_baudrate = 38400
    set_timeout = 3
    
    # Initialize IAI from class
    robot = IAI_Robot(set_port, set_baudrate, set_timeout)