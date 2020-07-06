#!/bin/bash

infile="$1";
# usually full.rec


extension=$([[ "$infile" = *.* ]] && echo ".${infile##*.}" || echo '')
   
base=${infile##*/}
directory=${infile%$base}
	    
base1=${base%$extension}

base2=${base1%_full}

echo -------   starting automatic flattening for $infile ----------------------

findsection -tomo $infile -si 20,1,20 -su flatten.mod
flattenwarp -i flatten.mod -ou flatten.tfm

warpvol -sa -i $infile -ou "$base1"_flattened.rec -x flatten.tfm


echo -------   starting automatic trimming for $infile ----------------------
#trimming

findsection -tomo "$base1"_flattened.rec -si 20,1,20 > trim.out

zlimits=`tail trim.out -n 1 | grep -o '[^:]\+$'`
zlim1=${zlimits/  /,}

trimvol -y $zlim1 -rx "$base1"_flattened.rec "$base2".rec


