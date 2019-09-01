#!/usr/bin/env bash

wapp="python3 /bin/wapp"

echo -n "Installing wapp ... "
mkdir code
cp wapp.py code
$wapp -c wapp wapp.control
rm -r code
$wapp -i wapp
echo "done"
