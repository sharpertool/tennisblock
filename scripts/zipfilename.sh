#!/usr/bin/env bash

zipfile=${ZIP_PREFIX}.gz

if [ ! -z "${CIRCLE_TAG}" ]
then
    zipfile=${ZIP_PREFIX}_${CIRCLE_TAG}.gz
else
    zipfile=${ZIP_PREFIX}_${CIRCLE_SHA1}.gz
fi

echo $zipfile


