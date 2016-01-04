#!/bin/bash
dir="/Users/lekha/galvanize/capstone/projectRiley/data/hadoopdata/2015-01-09/histories"
i=0
for filename in $dir/*.gz; do
    i=$((i+1))
    echo $i
    gzcat $filename | awk '/content:start:/,/content:end:/' | sed '1d' > output$i.html
done
