import socket
import sys, getopt
from termcolor import colored

#payload_example = '\x31\x00\x00\xff\x00\x00\xf0\x0f\x2f'

# All of the lamp individual local IP addresses
lamp_1 = 'IP_ADDRESS_OF_LAMP'
lamp_2 = 'IP_ADDRESS_OF_LAMP'
lamp_3 = 'IP_ADDRESS_OF_LAMP'
lamp_4 = 'IP_ADDRESS_OF_LAMP'
lamps = [lamp_1, lamp_2, lamp_3, lamp_4]

def main(argv):
    
    try:
        opts, args = getopt.getopt(argv, 'hb:', ['on', 'off'])
    except getopt.GetoptError:
        print 'lights.py -h for help'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'lights.py -on -off -b <brightness_level_percentage>'
            sys.exit()
        elif opt == '--on':
            send_payload_to_all_lamps('all_on')
            print colored('Turned all lamps on at 100% brightness.', 'blue')
        elif opt == '--off':
            send_payload_to_all_lamps('all_off')
            print colored('Turned off all lamps.', 'red')
        elif opt in ("-b", "--brightness"):
            send_payload_to_all_lamps('set_brightness ' + arg)
            print colored('Set brightness of all lamps to ' + arg + '%', 'blue')

    sys.exit()

def send_payload_to_all_lamps(command):
    
    payload = ''

    if command == 'all_on':
        payload = adjust_brightness_payload(100)
    elif command == 'all_off':
        payload = adjust_brightness_payload(0)
    elif command.startswith('set_brightness'):
        payload = adjust_brightness_payload(command.split()[1])

    for lamp in lamps:
        host = lamp
        port = 5577
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        print("Payload:" + payload)
        s.send(payload)
        s.close()


def create_payload():
    
    command_id = 0x31
    red_value = 0x00
    green_value = 0xff
    blue_value = 0x30
    warm_brightness = 0x00
    white_brightness = 0x00
    first_bool = 0xf0
    second_bool = 0x0f
    sum = command_id + red_value + green_value + blue_value + warm_brightness + white_brightness + first_bool + second_bool
    checksum = sum % 255 - int(sum/255)

    payload = chr(command_id) + chr(red_value) + chr(green_value) + chr(blue_value) + chr(warm_brightness) + chr(white_brightness) + chr(first_bool) + chr(second_bool) + chr(checksum)
    return payload

def adjust_brightness_payload(brightness_percentage):
    
    command_id = 0x31
    red_value = 0x00
    green_value = 0x00
    blue_value = 0x00
    warm_brightness = int(float(brightness_percentage)/100 * 255) #0xff
    white_brightness = 0x00
    first_bool = 0x0f
    second_bool = 0x0f
    sum = command_id + red_value + green_value + blue_value + warm_brightness + white_brightness + first_bool + second_bool
    checksum = sum % 255 - int(sum/255)
    
    payload = chr(command_id) + chr(red_value) + chr(green_value) + chr(blue_value) + chr(warm_brightness) + chr(white_brightness) + chr(first_bool) + chr(second_bool) + chr(checksum)
    return payload

if __name__ == "__main__":
    main(sys.argv[1:])
