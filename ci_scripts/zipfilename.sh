#!/usr/bin/env bash

zipfile=${ZIP_PREFIX}.gz

timestamp=$(date +%Y-%m-%d_%H-%M)

# Tag if specified, otherwise branch
ID=${CIRCLE_TAG:=${CIRCLE_BRANCH}_${CIRCLE_SHA1}}

zipfile="${ZIP_PREFIX}_${timestamp}_${ID}.gz"

echo $zipfile


