#!/bin/bash
echo "Hey you"
echo "What's your name?"
read NAME
if [[ $NAME == "Gustav" ]]; then
	echo "To hell with you"
	exit 1
else
	echo "Hello $NAME"
fi