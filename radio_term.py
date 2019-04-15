"""
Example for using the RFM9x Radio with Raspberry Pi.

Learn Guide: https://learn.adafruit.com/lora-and-lorawan-for-raspberry-pi
Author: Brent Rubell for Adafruit Industries
"""
# Import Python System Libraries
import time
# Import Blinka Libraries
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
# Import the SSD1306 module.
import adafruit_ssd1306
# Import RFM9x
import adafruit_rfm9x
#Add JSON support
import json

# Button A
btnA = DigitalInOut(board.D5)
btnA.direction = Direction.INPUT
btnA.pull = Pull.UP

# Button B
btnB = DigitalInOut(board.D6)
btnB.direction = Direction.INPUT
btnB.pull = Pull.UP

# Button C
btnC = DigitalInOut(board.D12)
btnC.direction = Direction.INPUT
btnC.pull = Pull.UP

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)




# 128x32 OLED Display
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x3c)

###############
def hw_scroll_off(self):
    self.write_cmd(SET_HWSCROLL_OFF) # turn off scroll
      
def hw_scroll_h(self, direction=True):   # default to scroll right
    self.write_cmd(SET_HWSCROLL_OFF)  # turn off hardware scroll per SSD1306 datasheet
    if not direction:
        self.write_cmd(SET_HWSCROLL_LEFT)
        self.write_cmd(0x00) # dummy byte
        self.write_cmd(0x07) # start page = page 7
        self.write_cmd(0x00) # frequency = 5 frames
        self.write_cmd(0x00) # end page = page 0
    else:
        self.write_cmd(SET_HWSCROLL_RIGHT)
        self.write_cmd(0x00) # dummy byte
        self.write_cmd(0x00) # start page = page 0
        self.write_cmd(0x00) # frequency = 5 frames
        self.write_cmd(0x07) # end page = page 7
         
    self.write_cmd(0x00)
    self.write_cmd(0xff)
    self.write_cmd(SET_HWSCROLL_ON) # activate scroll
###############
# Clear the display.
display.fill(0)
display.show()
width = display.width
height = display.height

## Get JSON
with open("PreSign-Prac.json", "r") as read_file:
    pstx = json.load(read_file)
    
################

#var IDK == 0
#while lateNight[IDK]<5
#    ("pkg"+lateNight[IDK])=lateNight[IDK]


#    datalen = length(pstx)
#    int cyc = 0
#    int numc = 1
#   while(datalen>240){
#    bytes[cyc,240*numc] = ("pkg"+numc)
#    cyc = cyc + 240
#    datalen = datalen - 240
#    }
    

##

# Configure LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
rfm9x.tx_power = 23
prev_packet = None

while True:
    packet = None
    # draw a box to clear the image
    display.fill(0)
    display.text('RasPi LoRa', 35, 0, 1)

    # check for packet rx
    packet = rfm9x.receive()
    if packet is None:
        display.show()
        display.text('- Waiting for PKT -', 15, 20, 1)
    else:
        # Display the packet text and rssi
        display.fill(0)
        prev_packet = packet
        packet_text = str(prev_packet, "utf-8")
        display.text('RX: ', 0, 0, 1)
        ##addding serial out for received to terminal and Log
#        send.text(packet_text.MISO) #      <-- this code is fake, but....stil....
        ###### Log Bit of code
#        log.text(packet_text.sendToLog.txt)
#        scribv = open('/home.pi/log_file.txt', 'w')
#        scribv.write(get_text())
#        scribv.close()
        ##
        display.text(packet_text, 25, 0, 1)
        distplay.hw_scroll_h()
        time.sleep(1)

    if not btnA.value:
        # Send Button A
        display.fill(0)
        button_a_data = bytes("Button A!\r\n","utf-8")
        rfm9x.send(button_a_data)
        display.text('Sent Button A!', 25, 15, 1)
    elif not btnB.value:
        # Send Button B
        display.fill(0)
        button_b_data = bytes("Button B!\r\n","utf-8")
        rfm9x.send(button_b_data)
        display.text('Sent Button B!', 25, 15, 1)
    elif not btnC.value:
        # Send Button C
        display.fill(0)
        button_c_data = bytes(pstx + "\r\n","utf-8")
        rfm9x.send(button_c_data)
        display.text('Sent JSON_C', 25, 15, 1)


    display.show()
    time.sleep(0.1)
