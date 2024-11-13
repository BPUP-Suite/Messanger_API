#!/bin/bash

ps axf | grep docker | grep -v grep | awk '{print "kill -9 " $1}' | sudo sh 
dockerd