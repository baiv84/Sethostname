#!/bin/sh

echo $1 > /etc/hostname
hostname -b $1
reboot
