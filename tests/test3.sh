#!/bin/bash

read -p "Enter empty:" INPUT
if [[ -n "$INPUT" ]]; then
	exit 1
fi
