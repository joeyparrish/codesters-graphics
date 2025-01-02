#!/bin/bash

# 190 => 164 => 96 => 

function crush() {
  cp "$1" "$1.backup"

  local old_size=$(cat "$1" | wc -c)

  pngcrush -rem allb -brute -reduce "$1" "$1.new" &>/dev/null
  mv "$1.new" "$1"
  optipng -o7 "$1" &>/dev/null

  local new_size=$(cat "$1" | wc -c)

  if (( new_size >= old_size )); then
    echo "Could not optimize."
    mv "$1.backup" "$1"
    return 1
  else
    rm "$1.backup"
    return 0
  fi
}

function check_quality() {
  psnr=$(compare -verbose -metric PSNR "$1" "$2" /dev/null 2>&1 | grep all: | cut -f 2 -d : | cut -f 1 -d .)

  if [[ "$psnr" == "inf" ]] || (( $psnr > 40 )); then
    return 0
  else
    return 1
  fi
}

for x in sprites/*.png; do
  echo "Processing $x..."
  first_size=$(cat "$x" | wc -c)

  convert "$x" png8:"$x.new.png"

  if check_quality "$x" "$x.new.png"; then
    echo "Reduced to 256 colors.  (PSNR: $psnr)"
    mv "$x.new.png" "$x"
  else
    echo "Reduction to 256 colors was too intense.  (PSNR: $psnr)"
    convert "$x" -colors 1024 "$x.new.png"

    if check_quality "$x" "$x.new.png"; then
      echo "Reduced to 1024 colors.  (PSNR: $psnr)"
      mv "$x.new.png" "$x"
    else
      echo "Reduction to 1024 colors was too intense.  (PSNR: $psnr)"
      rm "$x.new.png"
    fi
  fi

  echo "Optimizing encoding."
  crush "$x"
  final_size=$(cat "$x" | wc -c)
  echo "Reduced size by $(( first_size - final_size )) bytes."
done
