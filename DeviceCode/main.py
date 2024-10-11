RECAL = False

##########################
Gram_To_N = 0.00980665
#converts raw cell data to Newtons
global Force_Conversion
Force_Conversion = 0.0010024993202155026 * Gram_To_N
#########################

from Force import HX711
from machine import Pin, I2C, PWM
from vl53l0x import VL53L0X
from lcd1602 import LCD
from SDCardWriter import Name, mount, unmount
import _thread
import time

TEST = Pin(9, Pin.IN)
UP = Pin(5, Pin.IN)
DOWN = Pin(1, Pin.IN)

DIRECTION = Pin(26, Pin.OUT)
MOVEMENT = PWM(Pin(22))#Pin(26, Pin.OUT)

lcd = LCD()
#########################################
lcd.message('Press Test\nTo Continue')
while TEST.value() == 0:
    time.sleep(0.1)
#########################################
lcd.clear()
lcd.message('Starting...')
#load cell
cell = HX711(d_out=11, pd_sck=10)

#TOF sensor
sda = Pin(14)
scl = Pin(15)
id = 1

i2c = I2C(id=id, sda=sda, scl=scl)
tof = VL53L0X(i2c)

budget = tof.measurement_timing_budget_us
tof.set_measurement_timing_budget(40000)

tof.set_Vcsel_pulse_period(tof.vcsel_period_type[0], 12)

tof.set_Vcsel_pulse_period(tof.vcsel_period_type[1], 8)

def PWMFREQ(mm_min):
    PulsesPerRev = 25600#12800#6400#3200#1600#400
    ScrewPitch = 8
    freq = (PulsesPerRev*mm_min) / (ScrewPitch*60)
    freq = int(round(freq))
    return freq

#Load cell tare
def Calibration():
    lcd.clear()
    lcd.message('Calibrating...')
    Force = 0
    iteration = 100
    for i in range(iteration):
        Force += cell.read()
    tare = Force / iteration
    lcd.clear()
    lcd.message('Calibration\nFinished')
    time.sleep(0.75)
    lcd.clear()
    return tare

def TOFReject(prev, current, slope):
    accept = True
    if abs(current - prev) >= slope:
        accept = False
    return accept

def Line(tare, start_time):
    global Force_conversion
    Force = (cell.read() - tare) * Force_Conversion
    Distance = tof.ping() - 50
    time_passed = time.ticks_ms() - start_time
    return Force, Distance, time_passed


def Test():
    mount()
    with open("/sd/velocity.txt", "r") as file:
        TargetVelocity = float(file.read())
    file.close()
    print(f'Velocity: {TargetVelocity} mm/min')
    test = PWMFREQ(TargetVelocity)
    
    tof.ping()#primer to stop the sensor from presenting the max value for line one
    
    fullname = Name()
    start_time = time.ticks_ms()
    
    last_tick = 0
    refresh_tick = 1000
    
    prev = tof.ping()
    
    with open('/sd/'+fullname, "w") as file:
        file.write('Force(N),Distance(mm),Time(ms)\n')
        MOVEMENT.init(freq=test, duty_u16=32768)
        while True:
            data = Line(tare, start_time)
            file.write(f'{data[0]},{data[1]},{data[2]}\n')
            time_passed = data[2]
            time_lap = time_passed - last_tick
            
            if refresh_tick <= time_lap:
                last_tick = time_passed
                
                lcd.clear()
                Force = data[0]
                if abs(Force) == Force:
                    Force = round(Force,4)
                    Force = ' ' + str(Force)
                else:
                    Force = round(Force,4)
                lcd.message(f'{TargetVelocity} mm/min\n{Force} N')
                
            if float(data[1]) <= 0 and TOFReject(prev, data[1], 5):
                MOVEMENT.deinit()
                lcd.clear()
                lcd.message('Test Finished')
                break
            prev = data[1]        
    file.close()
    unmount()
    time.sleep(3)
    lcd.clear()
    lcd.message('Standby...')






try:
    mount()
    with open("/sd/velocity.txt", "r") as file:
        Recal = file.read()
    file.close()
    
except:
    Recal = 'skip'

if Recal == 'calibrate':
    lcd.clear()
    lcd.message('Calibration Mode')
    time.sleep(3)
    #Moves jaws upward for calibration
    DIRECTION.value(1)
    CalibrateSpeed = PWMFREQ(300)
    MOVEMENT.init(freq=CalibrateSpeed, duty_u16=32768)
    ping = (tof.ping() - 50)
    prev = (tof.ping() - 50)
    cont = True
    while cont:
        #if the point is valid(doesn't jump off to an absurdly large or small number)
        #and the point is <= 0 then it cuts the loop stopping the system from moving upward
        if ping <= 0 and TOFReject(prev, ping, 5):
            cont = False
        prev = ping
        ping = (tof.ping() - 50)
    MOVEMENT.deinit()
        
    while True:
        time.sleep(0.1)
        fullname = Name()
        calRange = 1000
        lcd.clear()
        lcd.message('Collecting Data')
        
        with open('/sd/'+fullname, "w") as file:
            file.write('Force(N)\n')
            
            prevProg = -1
            for i in range(calRange):
                Force = cell.read()
                file.write(f'{Force}\n')
                
                progress = round(100*i/calRange)
                if progress != prevProg:
                    prevProg = progress
                    lcd.clear()
                    lcd.message(f'Resting Data\n{progress}%')
                
            lcd.clear()
            lcd.message('Fix Mass to Jaws\nThen Press Test')
            while True:
                time.sleep(0.1)
                if TEST.value() == 1:
                    break
                
            prevProg = -1
            for i in range(calRange):
                Force = cell.read()
                file.write(f'{Force}\n')
                progress = round(100*i/calRange)
                if progress != prevProg:
                    prevProg = progress
                    lcd.clear()
                    lcd.message(f'Load Data\n{progress}%')
        unmount()
                
        lcd.clear()
        lcd.message(f'Data In\n{fullname}')
        while TEST.value() != 1:
            time.sleep(0.1)
        mount()
else:
    last_tick = time.ticks_ms()
    time_passed = time.ticks_ms()
    refresh_tick = 1000
    
    short = 1
    TargetStandby = 300
    standby = PWMFREQ(TargetStandby)
    
    global tare
    tare = Calibration()

    lcd.clear()
    
    while True:
        time_passed = time.ticks_ms()
        time_lap = time_passed - last_tick
        
        if refresh_tick <= time_lap:
            last_tick = time_passed
                
            lcd.clear()
        
            Force = (cell.read() - tare) * Force_Conversion
        
            if abs(Force) == Force:
                Force = round(Force,4)
                Force = ' ' + str(Force)
            else:
                Force = round(Force,4)
            lcd.message(f'Standby\n{Force} N')
            
        time.sleep(0.1)
        Busy = 0
        if TEST.value() == 1:
            DIRECTION.value(1)
            lcd.clear()
            lcd.message('Begining test')
            time.sleep(0.5)
            try:
                Test()
            except:
                lcd.clear()
                lcd.message('Error!\nIssue With SD Card!')
                time.sleep(3)

        if DOWN.value() == 1 and UP.value() == 1:
            tare = Calibration()
            
        elif UP.value() == 1 and Busy != 1:
            Busy = 1
            DIRECTION.value(1)
            MOVEMENT.init(freq=standby, duty_u16=32768)

        elif DOWN.value() == 1 and Busy != 2:
            Busy = 2
            DIRECTION.value(0)
            MOVEMENT.init(freq=standby, duty_u16=32768)
        
        else:
            Busy = 0
            MOVEMENT.deinit()





