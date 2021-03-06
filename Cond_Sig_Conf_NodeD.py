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

nodeA = "0x1234123412341234123412341234123412341234123412341234"
nodeB = "0xabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd"
nodeC = "0x12ab12ab12ab12ab12ab12ab12ab12ab12ab12ab12ab12ab12ab"
nodeD = "0x23cd23cd23cd23cd23cd23cd23cd23cd23cd23cd23cd23cd23cd"
nodeE = "0x007007007007007007007007007007007007007007007007007X"
nodeA_pSig = 'Tx approved: Rad1935'
nodeB_pSig = 'Tx approved: Fly1903'
nodeC_pSig = 'Tx approved: Cal1876'
nodeD_pSig = 'Tx approved: '
nodeE_pSig = 'Tx approved: '
str(nodeA)
str(nodeB)
str(nodeC)
str(nodeD)
str(nodeE)
str(nodeA_pSig)
str(nodeB_pSig)
str(nodeC_pSig)
str(nodeD_pSig)
str(nodeE_pSig)

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

# Clear the display.
display.fill(0)
display.show()
width = display.width
height = display.height

## Get JSON
#with open("ETH_BTC-Alpha.json", "r") as read_file:
#    pstx = json.load(read_file)
#str(pstx)
#print(pstx)
################
# Configure LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
rfm9x.tx_power = 23
prev_packet = None
print("WELCOME TO OVERLINE")
while True:
    packet = None
    # draw a box to clear the image
    display.fill(0)
    display.text('Overline', 35, 0, 1)
#    display.text('-SEND-', 40, 20, 1)
    display.show()
#    print("made it to 'Overline")

    # check for packet rx
    packet = rfm9x.receive()
    if packet is None:
        display.show()
        display.text('- Node A Receiving -', 12, 20, 1)
#        print("node receiving nothing")
    
    else:
        # Display the packet text and rssi
        print("made it into the else statement. woo.")
        display.fill(0)
        display.text("Tx Received", 20, 0, 1)
        display.show()
        time.sleep(1)
#        log = open("rec_log.txt", "w")
        prev_packet = packet
        packet_text = str(prev_packet, "utf-8")
        print(packet_text)
#        log.write(packet_text + "/r/n")
#        log.close()
        if packet_text == nodeD:
            exit
        elif packet_text[:11] == "Tx approved":
            print('relaying momentum')
            display.fill(0)
            print("Relaying Tx!")
            display.text('Tx Relay Request', 0, 0, 1)
            display.text('Approved for Passage', 0, 20, 1)
            display.show()
            time.sleep(1)
            button_b_data = bytes(packet_text,"utf-8")
            rfm9x.send(button_b_data)
            display.fill(0)
            display.text('Relay Successful', 0, 0, 1)
            display.text('X.XXXXX NRG Collected', 0, 20, 1)
            display.show()
            print('relay message sent')
            time.sleep(1)
        else:
            display.fill(0)
            print('tx request discovered')
            display.text('Transaction Found', 0, 0, 1)
            display.show()
            time.sleep(1)
            while True: #btnA.value == True & btnC.value == True:
                display.fill(0)
                display.text('Submit PoD Claim?', 0, 0, 1)
                display.text('YES', 0,20,1)
                display.text('NO', 110,20,1)
                display.show()
                display.fill(0)

                if btnA.value == False:
                    time.sleep(1)
                    display.fill(0)
                    display.text("Generating PoD...", 10, 15, 1)
                    print('"YES" selected')
                    button_a_data = bytes(nodeD_pSig,"utf-8")
                    rfm9x.send(button_a_data)
                    print('pSig should be sent...?')
                    display.fill(0)
                    x=15
                    minX = -6 * len(nodeD_pSig) # 12 = 6 pixels/character * text size 2
                    while x > minX:
                        display.fill(0)
                        display.text(nodeD_pSig, x, 0, 1)
                        display.show()
                        x = x-4
                    display.fill(0)
                    display.text('PoD Entry Sent', 25, 15, 1)
                    time.sleep(1.5)
                    print('PoD entry sent')
                    display.fill(0)
                    break
                elif btnC.value == False:
                    display.fill(0)
                    display.text('Declined PoD Entry', 15, 15, 1)
                    time.sleep(1.5)
                    display.fill(0)
                    break
    if not btnB.value:
        # Send Button B
        display.fill(0)
        print("Button Script Running!")
        button_b_data = bytes(nodeD,"utf-8")
        rfm9x.send(button_b_data)
        display.text('Sent Transaction', 25, 15, 1)
display.show()
time.sleep(0.1)
