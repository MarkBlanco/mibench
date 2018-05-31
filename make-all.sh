#!/bin/bash

# A script to make all the MiBench tests for an embedded target.
declare -a srcdirs=(
	"automotive/basicmath"
    "automotive/bitcount"
    "automotive/qsort"
    "automotive/susan"
    "consumer/jpeg/jpeg-6a"
    "consumer/tiff-v3.5.4"
    "consumer/typeset/lout-3.24"
    #"consumer/mad/mad-0.14.2b"
	"consumer/lame/lame3.70"
    "office/ispell"
    #"office/rsynth"
    #"office/sphinx"
	"office/stringsearch"
    "security/blowfish"
    #"security/pgp"
	"security/rijndael"
    "security/sha"
    #"telecomm/adpcm/src"
	"telecomm/CRC32"
    "telecomm/FFT"
    #"telecomm/gsm"
	)



export CC=gcc #arc-linux-uclibc-gcc
export RUNIT=run-remote.sh

BASE_DIR=$(pwd)

for d in ${srcdirs[@]}
do
    echo ${d}
    cd ${d}
    # ./configure # Sometimes necessary...
    make clean
    make 
    cd $BASE_DIR
done
