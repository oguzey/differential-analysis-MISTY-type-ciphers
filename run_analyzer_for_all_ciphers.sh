#!/bin/bash

_logpath="$(pwd)/logs"
mkdir -p $_logpath

pattern="import systems, cipher_name"

cd dp_analyzer
for systems in $(find ./data -name "*.py" -not -name "vars.py" -not -name "__init__.py" | sort)
do
    _name=$(basename ${systems})
    _name=${_name%.py}
    echo -e "Current time is $(date +"%T:%3N").**Start analyze systems '${_name}'." | column -s "**" -t
    sed -i "/${pattern}/c\    from data.${_name} import systems, cipher_name" ./analyzer.py
    ./analyzer.py --logdir $_logpath > $_logpath/${_name}.log
done
