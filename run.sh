#!/bin/sh
GOOS=js GOARCH=wasm go build -o hello_world.wasm
wasm2c -o hello_world.c hello_world.wasm
./ana.py hello_world.c > report.txt

