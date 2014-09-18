#!/bin/bash
LOCALES=$*

for LOCALE in ${LOCALES}
do
    echo "NNJoin/i18n/NNJoin_"${LOCALE}".ts"
    # Note we don't use pylupdate with qt .pro file approach as it is flakey
    # about what is made available.
    lrelease-qt4 i18n/NNJoin_${LOCALE}.ts
done
