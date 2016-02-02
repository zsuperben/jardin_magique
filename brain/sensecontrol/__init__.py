__author__ = 'zsb'

import ConfigParser
import _hashlib


# This controls the new sensors detection mechanism, and when it detects a new sensor it will add some more
# details into django gui. Where user can specify a configuration, and customise it.
# Then it uploads the new configuration and code to the sensor device.



# First bit we need to have a WiFi scanner, that will detect the special SSID of a new sensor.
# this should be a daemon.

# This daemon the creates a new database record for the sensor.

# This new record is then showed in django along with some options to configure the module.

# a new key pair is created to secure exchange with the sensor.

# The form in django is then trans  lated into a C code, compiled and uploaded to  the module.