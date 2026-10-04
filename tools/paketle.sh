#!/bin/bash
# Eski ad: artık tools/teslim.sh iki zip üretir (maket + kaynak). Aynı bağımsız değişkenler:
# tools/paketle.sh <render_kök> <node_modules> <çıktı_klasörü> [python]
exec "$(dirname "$0")/teslim.sh" "$@"
