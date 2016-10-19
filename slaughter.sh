#!/bin/bash

# Careful : this program kills ALL your simulations without confirmation

tokill=$(oarstat | grep $USER | cut -d ' ' -f 1)
oardel $tokill