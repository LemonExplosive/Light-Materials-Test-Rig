#SD Card writer
import sdcard
import uos
import machine
import utime

def mount():
    cs = machine.Pin(17, machine.Pin.OUT)
    cs.value(1)

    spi = machine.SPI(0,
                    baudrate=1000000,
                    polarity=0,
                    phase=0,
                    bits=8,
                    firstbit=machine.SPI.MSB,
                    sck=machine.Pin(18),
                    mosi=machine.Pin(19),
                    miso=machine.Pin(16))

    sd = sdcard.SDCard(spi, cs)
    vfs = uos.VfsFat(sd)
    uos.mount(vfs, "/sd")

def Name():

    Dir_List = []
    Dir_List = uos.listdir('/sd')
    print("From DIR_LIST -->", Dir_List)
    FileName = 'PullTest'
    extension = '.csv'
    matches = True
    iteration = 0
    default = FileName
    while matches:
        matches = False
        for i in Dir_List:
            fullname = FileName + extension
            if i == fullname:
                matches = True
                FileName = default + str(iteration)
        iteration += 1
    print(fullname)
    return fullname

def unmount():
    uos.umount("/sd")
