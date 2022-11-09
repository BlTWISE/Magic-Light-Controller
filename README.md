# Magic-Light-Controller

Don't really feel like describing this in great detail but this is a basic script that has the capability to control my smart lights. The brand name has magic in it but I forget the exact name. I may re-visit this later.

The protocol for the light commands is about 85% fully reversed. Other smart lights may have similar command/payload structures.

# Brif Revisit ... 11/9/2022

Briefly ran into this again in pursuit of something else, but I know someone might Google this problem in a similar mindstate to when I was before I made this. Frankly, confusing, and especially if you have a weird brand. However, many lights at the time that this was created and possibly still now use similar protocols and payloads. You can learn a lot from this example, even if it isn't an exact match for your model. I also kept it as simple as possible so it's easy to absorb the methodology of how you could use this in a practical sense. Here's the most important/significant highlights, the reversed payloads which includes colors, brightness, a checksum, and more:
```python
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
```
And sending it to the lights via a socket:
```python
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
```
