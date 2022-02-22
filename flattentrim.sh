#!/bin/bash
module load IMOD/BETA4.10.31
source $EBROOTIMOD/IMOD-linux.sh

infile="$1";
# usually full.rec

extension=$([[ "$infile" = *.* ]] && echo ".${infile##*.}" || echo '')
   
base1=${base%$extension}

echo 
echo 
echo -------   starting automatic flattening for $infile ----------------------
echo 

findsection -tomo $infile -si 20,1,20 -su flatten.mod
flattenwarp -i flatten.mod -ou flatten.tfm

warpvol -sa -i $infile -ou "$base1"_flattened.rec -x flatten.tfm

echo 
echo 
echo -------   starting automatic trimming for $infile ----------------------
echo 
#trimming

findsection -tomo "$base1"_flattened.rec -si 20,1,20 > trim.out

zlimits=`tail trim.out -n 1 | grep -o '[^:]\+$'`
zlim1=${zlimits/  /,}

trimvol -y $zlim1 -rx "$base1"_flattened.rec "$base1"_final.rec


