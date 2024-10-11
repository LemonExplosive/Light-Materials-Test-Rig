#This program demonstrates reading and writing to a micro SD card using the driver from here
#https://raw.githubusercontent.com/micropython/micropython/master/drivers/sdcard/sdcard.py
#The creator of this source code is Digikey and this is where you can find the original story about this...
#https://www.digikey.com/en/maker/projects/raspberry-pi-pico-rp2040-sd-card-example-with-micropython-and-cc/e472c7f578734bfd96d437e68e670050

#You will need an SD Card adapter / Breakout board with SPI interface - Link provided on our companion website
#Wire it up to your pico per the frizting diagram.
#Insert a FAT32 formatted SD Card into the slot and run the following program

import machine
import sdcard
import uos

# Assign chip select (CS) pin (and start it high)
cs = machine.Pin(17, machine.Pin.OUT)    #set pin GPIO 9 as output for use as Chip Select on SPI interface
cs.value(1)                             #set the pin to high 

# Intialize SPI peripheral (start with 1 MHz)
spi = machine.SPI(0,                           #Configure the SPI interface
                  baudrate=1000000,
                  polarity=0,
                  phase=0,
                  bits=8,
                  firstbit=machine.SPI.MSB,
                  sck=machine.Pin(18),        #PICO GPIO Pin 10
                  mosi=machine.Pin(19),       #PICO GPIO Pin 11
                  miso=machine.Pin(16))        #PICO GPIO Pin  8

# Initialize SD card
sd = sdcard.SDCard(spi, cs)                   

# Mount filesystem
vfs = uos.VfsFat(sd)
uos.mount(vfs, "/sd")
print(uos.listdir('/sd'))  #print out contents of directory of /sd

#You can also load the contents of the directory listing into a list for processing
Dir_List = []
Dir_List = uos.listdir('/sd')
print("From DIR_LIST -->", Dir_List)


# Write some data to SD card in a manor similar to a data logger
# Note, text (String) data is used to write to the file, not numerical data in variables
# If not file exists, it will be created.
# If the file exists with data, that data will be overwritten
print("Write some data")
with open("/sd/test01.txt", "w") as file:                   #open a file or create a file for writing
    L = 0                                                   #counter variable
    file.write("This is my data for the data logger\r\n")   #Write line of text to file with carriage return and line feed

    while L < 10:                                           #loop 10 times to write 10 lines of data
        data_s = str(L) + " line of data.\r\n"              #Create a variable containing the line of data with carriage return and line feed
        file.write(data_s)                                  #Write the variable containing the data to the file
        L += 1                                              #Increment counter
        print(L)

# Read all the contents of the file that was created
# IMPORTANT!!!! Even though we wrote all that data to the SD Card, it does not mean all that data
# will fit in the SRAM.  The PICO has a limitted amount of ram.
with open("/sd/test01.txt", "r") as file:                   # Open the file for reading
    data_s = file.read()                                    # Read contents of file into variable data_s
    print("SD ",data_s)                                     # print all the contents of the file


#Now lets put the data into a LIST so each line can be processed
List_Of_Data = []       # List that will contain lines of data
EOL = "\r\n"            # End of line delimitter
L_Len = len(data_s)     # Measure size of data

while L_Len > 0:                            # Run loop until all the data is consumed
    Index = data_s.find(EOL, 0, L_Len)      # Find location of end of first line and record that position
    List_Of_Data.append(data_s[0:Index])    # Copy that line of data into the list
    Comp_Line = Index + 2                   # Total # of chars is line len + 2 for "\c\n" slashes are not counted
    data_s = data_s[Comp_Line:L_Len]        # Delete the current line of data from source variable
    L_Len = len(data_s)                     # Update Line length variable

print("\n\n")

item = 0                          # Variable used for indexing through the list
while item < len(List_Of_Data):   # Loop until index equals len of the list
    print(List_Of_Data[item])     # Print the item in the list
    item += 1                     # Increment the list index variable

print("ALL DONE!")
    