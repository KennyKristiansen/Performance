"""Extract data from PLC and plot"""

import json
import struct
import time

import snap7
from numpy import real

IP: str = "192.168.73.2"
client = snap7.client.Client()
client.set_connection_params(address=IP, local_tsap=0, remote_tsap=1)
client.connect(address=IP, rack=0, slot=1)
connectionStatus = client.get_connected()
print(f"Connected: {connectionStatus}")

# Start new test


def startTest():
    startTime = time.time()
    expectedCycleTime_ms = 2
    expectedWaitTime = (expectedCycleTime_ms / 1000) * 256 * 64
    exptectedEndTime = startTime + expectedWaitTime

    client.db_write(3, 2064, int(11).to_bytes(1, "big"))
    response = True

    print("Running test from PLC")
    while response == True:
        response = client.db_read(3, start=2064, size=1)
        response = struct.unpack(">B", response[0:2])[0]
        response = bool(response - 10)
        print(
            f"Expected time left: {exptectedEndTime - time.time():.0f} seconds    ",
            end="\r",
        )
        time.sleep(expectedCycleTime_ms)
    print(f"wait time was {time.time() - startTime}")
    print("Performance test finished")


def extract(filename):
    dbPlotData: list = []
    dbNumber: int = 3
    dbStartByte: int = 1036  # byte offset from extract_times
    dataSize: int = 4  # PLC datatype is Real
    dataCount: int = 256  # arraysize of Real

    functionValues = {}
    for function in range(0, 64):
        client.db_write(3, 2060, function.to_bytes(2, "big"))
        time.sleep(0.01)
        datapoints = []
        print(f"Extracting {function} out of {63}", end="\r")

        response = client.db_read(
            dbNumber, start=dbStartByte, size=dataSize * dataCount
        )
        for byte in struct.iter_unpack(">f", response):
            datapoints.append(float(byte[0]))
        functionValues[function] = datapoints
    dbPlotData.append(functionValues)

    filename = filename + ".json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(dbPlotData, f, indent=4)


startTest()

extract(filename="changed_conveyor")
