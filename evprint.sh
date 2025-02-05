#!/bin/bash

while true
do
  sleep 3
  script -q -c "./bin/evoutput" /tmp/evlog.txt
  ISXBOX="$(cat /tmp/evlog.txt | awk '/Xbox Wireless Controller[[:space:]]*$/')"

  if [ -z "${ISXBOX}" ]; then
    echo "Didn't find Xbox Controller event!"
    echo "" > ./xboxevent.txt
    continue
  fi

  echo "Found Xbox Controller event!"
  echo $ISXBOX | grep -oP '[^/]+(?=:)' > ./xboxevent.txt
done
