#!/bin/sh
# If a Mail-in-a-Box management directory exists
# then append it to the commamnd search path.
if [ -d "/root/mailinabox/management" ] ; then
  PATH="$PATH:/root/mailinabox/management"
fi
