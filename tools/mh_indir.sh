#!/bin/bash
# İnsan modeli verisi (MakeHuman, CC0) — repoya konmaz; bu betikle indirilir.
# Kullanım: tools/mh_indir.sh <hedef_klasör>   sonra: export EGE_MH=<hedef_klasör>
set -e
H=${1:?hedef klasör}
mkdir -p "$H"; cd "$H"
B=https://raw.githubusercontent.com/makehumancommunity/makehuman/master/makehuman/data
curl -sSfL -o base.obj "$B/3dobjs/base.obj"
curl -sSfL -o default.mhskel "$B/rigs/default.mhskel"
curl -sSfL -o default_weights.mhw "$B/rigs/default_weights.mhw"
# vücut hedefleri (yaş/cinsiyet/kilo): PyPI tekerleğinin içindeki targets.npz
curl -sSfL -o mh.whl https://files.pythonhosted.org/packages/py3/m/makehuman/makehuman-1.3.2-py3-none-any.whl
python3 -c "import zipfile; open('targets.npz','wb').write(zipfile.ZipFile('mh.whl').read('makehuman/data/targets.npz'))"
rm -f mh.whl
ls -la
