import sys
import os
import subprocess
from time import sleep
import wave
import pyaudio


chunk=1024


def prompt_sound(sound_type):

        if sound_type == "prompt":
            f = wave.open(r"prompt.wav","rb")
        elif sound_type == "alert_low_battery":
            f = wave.open(r"battery_percentage_below_threshold.wav","rb")
        else:
            return

        p = pyaudio.PyAudio()
        stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
        channels = f.getnchannels(),  
        rate = f.getframerate(),
        output = True)
    
        #read data  
        data = f.readframes(chunk)  

        #paly stream  
        while data != '':  
            stream.write(data)  
            data = f.readframes(chunk)  

        #stop stream  
        stream.stop_stream()  
        stream.close()  

        return;

def get_battery_percentage():

    cmd = [ 'upower', '-i', '/org/freedesktop/UPower/devices/battery_BAT0' ]

    # data = subprocess("upower -i /org/freedesktop/UPower/devices/battery_BAT0")

    output = subprocess.Popen( cmd, stdout=subprocess.PIPE ).communicate()[0]

    result = output.split("percentage:")[-1].split("\n")[0].strip()
    result = result.replace("%", "")
    result = int(result)

    return result

if __name__ == '__main__':
    try:
        int(sys.argv[1])
    except:
        raw_input("*** Unable to read battery percentage threshold in command line argument. Press enter to exit : ***")
        exit()

    while True:
        battery = get_battery_percentage()

        if  battery < int(sys.argv[1]):
            print("\n\n*** Battery percentage : {}% less than {}% ***\n\n".format(battery, sys.argv[1]))
            prompt_sound("prompt")
            prompt_sound("alert_low_battery")

        elif  battery == int(sys.argv[1]):
            print("\n\n*** Battery percentage : {}% equals to  {}% ***\n\n".format(battery, sys.argv[1]))
            prompt_sound("prompt")
            prompt_sound("alert_low_battery")

        else:
            print("\n\nHave Enough battery : {}% above threshold {}%\n\n".format(battery, sys.argv[1]))

        sleep(20)