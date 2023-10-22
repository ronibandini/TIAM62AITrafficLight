# No Green No Helmet
# Am62A IA Traffic Light
# Roni Bandini @RoniBandini
# October 2023 MIT License
# https://bandini.medium.com

import subprocess
import time
import requests
import json

output_file = open('output.txt', 'w')
serverUrl='http://YourServer/yourfolder/'
noHelmetDetected=0
confidenceLimit=0.6

print("No helmet no green")
print("Prototype for Texas Instruments AM62A with Edge Impulse")
print("Roni Bandini, October 2023, Argentina, @RoniBandini")
print("")
print("Stop with CTRL-C")

# Impulse Runner in a subprocess sending the output to a file
subprocess.Popen(["edge-impulse-linux-runner", "--force-engine tidl", "-force-target", "runner-linux-aarch64-am62a"], stdout=output_file)

with open("output.txt", "r") as f:
    lines_seen = set()
    while True:

        line = f.readline()

        if not line:
            time.sleep(1)
            continue

        if ("[]" in line):

            print("No rider detected")
            # update Server
            if noHelmetDetected==1:
                noHelmetDetected=0
                print("Updating server")
                r = requests.get(serverUrl+'updateHelmet.php?nohelmet=0')
                print("Done...")
            else:
                print("Not updating server")

        print("Debug: "+str(line))

        if ("height" in line):

            if ("nohelmet" in line) and line not in lines_seen:
                print("Rider with no helmet")

                parts = line.split()
                myLine = parts[2][1:-1]

                howManyRecords=myLine.count('{')
                if howManyRecords==1:
                    myJson = json.loads(myLine)
                    confidence=float(myJson["value"])
                    print("Confidence: "+str(confidence))
                    lines_seen.add(line)

                    # update Server, checking last state first
                    if noHelmetDetected==0 and confidence>confidenceLimit:
                        noHelmetDetected=1
                        print("Updating server")
                        r = requests.get(serverUrl+'updateHelmet.php?nohelmet='+str(myJson["value"]))
                        print("Done...")
                    else:
                        print("Not updating server")

                else:
                    print("Malformed record")
                    myLine=""

            elif ("helmet" in line) and line not in lines_seen:
                print("Rider with helmet")
                parts = line.split()
                myLine = parts[2][1:-1]
                howManyRecords=myLine.count('{')
                if howManyRecords==1:

                    myJson = json.loads(myLine)
                    print("Confidence: "+str(myJson["value"]))

                    lines_seen.add(line)

                    # update Server
                    if noHelmetDetected==1 and confidence>confidenceLimit:
                        noHelmetDetected=0
                        print("Updating server")
                        r = requests.get(serverUrl+'updateHelmet.php?nohelmet=0')
                        print("Done...")
                    else:
                        print("Not updating server")
                else:
                    print("Malformed record")
