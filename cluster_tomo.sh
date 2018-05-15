#!/bin/bash

workdir="$1";
directive="$2";

# indir="/g/emcf/tomograms/in";
# outdir="/g/emcf/tomograms/in";
# 
# indir="../test/";
# outdir="../test/out";

# imodlatest='/g/emcf/software/imod_latest/IMOD';



# export IMOD_DIR=$imodlatest;
# export IMOD_CALIB_DIR=/g/emcf/software/ImodCalib;

tomouser=`whoami`;

cd $workdir

find . -type f -iname '*.st' -or -iname '*.mrc'  | while IFS= read -r  file ;do
#      printf 'File found: '"'%s'"'\n' "$file"

#  	    curr_user=`stat -c %U "$file"`
#  	    echo $curr_user		    
    
 	    
 	    extension=$([[ "$file" = *.* ]] && echo ".${file##*.}" || echo '')
 	    
	    
  	    base=${file##*/}
#    	    echo $base
 	    directory=${file%$base}
 	    
 	    
  	    base1=${base%$extension}
# 	    echo $base1


  	    ext1=${extension,,}
#    	    echo $ext1

	    dir1=${directory:2}
	    dir1=$workdir $dir1
#  	    echo $dir1
	    
# 	    tomotype=${dir1%%/*}
# 	    echo $tomotype

	    
#  	    case $tomotype in
#  	    D|D-*)
# 	      base2=${base%a$extension}
# 	      base2=${base2%b$extension}	      
#      
# 	      echo $curr_user > "$tmpdir/user_file--$base2$ext1"
# 	      echo $dir1 >> "$tmpdir/user_file--$base2$ext1"
# 	      ;; 	    
# 	    *)     
# 
# 	       echo $curr_user > "$tmpdir/user_file--$base1$ext1"
# 	       echo $dir1 >> "$tmpdir/user_file--$base1$ext1"
# 	      ;;
# 	    esac	    
#  	    
# 
#     	   cp "$file" "$tmpdir/$base1$ext1"
#   	   
#     	    [ -f "$tmpdir/user_file--$base1$ext1" ] && continue
#  	    

if [ -e $base1.rec ]
then
    echo "skipping "$base" because it already exists."
else
    echo "submitting "$base" to the cluster for automatic reconstruction."
    sbatch /g/emcf/schorb/code/cluster/tomo_submit.sh $base $dir1 $directive
fi


    	#  
	   
done 