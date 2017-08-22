#!/bin/bash

mkdir -p logs

pattern="import systems, cipher_name"

for systems in $(find ./data -name "*.py" -not -name "vars.py" -not -name "__init__.py" )
do
    _name=$(basename ${systems})
    _name=${_name%.py}
    echo -e "Start analyze systems '${_name}'. Current time is '$(date)'"
    sed -i "/${pattern}/c\    from data.${_name} import systems, cipher_name" ./analyzer.py
    ./analyzer.py > ./logs/${_name}.log
done
