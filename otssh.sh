#!/bin/bash

CONFIG="$HOME/.otssh_config"

touch $CONFIG

add() {
    echo "$1|$2|$3|$4|$5" >> $CONFIG
    echo "$1 added"
}

list() {
    cut -d'|' -f1 $CONFIG
}

list_detail() {
    while IFS='|' read -r name host user port identity
    do
        cmd="ssh"
        [ -n "$identity" ] && cmd="$cmd -i $identity"
        [ -n "$port" ] && [ "$port" != "22" ] && cmd="$cmd -p $port"
        cmd="$cmd $user@$host"
        echo "$name: $cmd"
    done < $CONFIG
}

update() {
    grep -v "^$1|" $CONFIG > temp
    mv temp $CONFIG
    echo "$1 updated"
}

delete_conn() {
    grep -v "^$1|" $CONFIG > temp
    mv temp $CONFIG
    echo "$1 deleted"
}

connect() {
    line=$(grep "^$1|" $CONFIG)
    if [ -z "$line" ]; then
        echo "[ERROR]: Server not found"
        exit
    fi

    IFS='|' read -r name host user port identity <<< "$line"

    cmd="ssh"
    [ -n "$identity" ] && cmd="$cmd -i $identity"
    [ -n "$port" ] && [ "$port" != "22" ] && cmd="$cmd -p $port"
    cmd="$cmd $user@$host"

    echo "Connecting to $name..."
    eval $cmd
}

case "$1" in
    add)
        add $3 $5 $7 $9 ${11}
        ;;
    ls)
        if [ "$2" == "-d" ]; then
            list_detail
        else
            list
        fi
        ;;
    update)
        update $3
        ;;
    rm)
        delete_conn $2
        ;;
    connect)
        connect $2
        ;;
    *)
        echo "Usage:"
        echo "./otssh.sh add -n name -h host -u user [-p port] [-i key]"
        echo "./otssh.sh ls [-d]"
        echo "./otssh.sh update -n name"
        echo "./otssh.sh rm name"
        echo "./otssh.sh connect name"
        ;;
esac
