#!/usr/bin/env python

# Copyright (c) 2020 Cisco Systems, Inc. and/or its affiliates

# Made for Python 3

import os
import time
import logging
import serial

debug = False;

if __name__ == "__main__":

    # Location of the directory to store log file, otherwise use /tmp
    log_file_dir = os.getenv("CAF_APP_LOG_DIR", "/tmp")
    log_file_path = os.path.join(log_file_dir, "iox-serial-port.log")

    # set up logging to file
    logging.basicConfig(
        filename=log_file_path,
        level=logging.INFO,
        format='[%(asctime)s]{%(pathname)s:%(lineno)d}%(levelname)s- %(message)s',
        datefmt='%H:%M:%S'
    )

    # set up logging to console
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)

    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)

    # add the handler to the root logger
    logging.getLogger('').addHandler(console)
    logger = logging.getLogger(__name__)

    logger.info('Starting application...')

    logger.info('Legend:\n  0 = dio contact closed,\n  1 = dio contact open,\n'+
        '  - = dio port not available in this app')

    # IR_SERIAL is the "label" of the serial port when IOx application 
    # is activated. In the absence of such variable we assume the 
    # serial device is /dev/ttySerial
    serial_device = os.getenv("IR_SERIAL", "/dev/ttySerial")

    # Open serial device
    try:
        ser = serial.Serial(serial_device)
    except:
        logger.info('Can\'t open port ' + serial_device); 
        exit(1)

    # Loop forever. We do not want that container to stop, do we?
    while (True):
        output = "";
        if ser.inWaiting() > 0:
            # We got at least one byte waiting for us
            s = ser.read(ser.inWaiting())
            s = s.decode('UTF-8')
        
            # print on log file, and echo back to serial port
            logger.info("Read >> [" + str(s) + "]")
            ser.write(str("["+ str(s)+"]").encode())

        time.sleep(2)

    logger.info("All done. Goodbye!\n")
