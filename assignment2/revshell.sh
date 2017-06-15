#!/bin/bash

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

     byte1=`echo "obase=16; if(${ip[3]}<16) print 0; ${ip[3]}" | bc`
     byte2=`echo "obase=16; if(${ip[2]}<16) print 0; ${ip[2]}" | bc`
     byte3=`echo "obase=16; if(${ip[1]}<16) print 0; ${ip[1]}" | bc`
     byte4=`echo "obase=16; if(${ip[0]}<16) print 0; ${ip[0]}" | bc`

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
        port=`echo "\x${v:2:2}\x${v:0:2}" | tr '[:upper:]' '[:lower:]'`
else
        echo "Invalid port specified."
        exit 1
fi

echo $part_1$port$part_2
