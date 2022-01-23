#!/bin/bash -eux
#
# usage:
#   check_diff-highlight.sh path
#
# description:
#   create link to ${path}
TARGET="diff-highlight"
MANAGER=""
ARRAY=""
OUT=${1:-}
DIR=""
FOUND=false

# diff-highlight needs git
if !(type git > /dev/null 2>&1); then
	echo "WARN: git is not installed." 1>&2
	exit 1
fi

# diff-higtlight location is searched by hpackage manager
if (type "dpkg" > /dev/null 2>&1); then
	MANAGER="dpkg -L"
elif (type "rpm" > /dev/null 2>&1); then
	MANAGER="rpm -ql"
else
	echo "WARN: package manager can't detect." 1>&2
	exit 1
fi

TARGET_LIST=($(${MANAGER} git | grep "/${TARGET}$"))

for f in ${TARGET_LIST[@]}; do
	if [ -f ${f} ]; then
#		ln -s ${f} ${OUT}
		echo ${f}
		FOUND=true
	elif [ -d ${f} ]; then
		DIR=${f}
	else 
		:
	fi
done

if "${FOUND}"; then
	echo "Create link from '${f}' to '${OUT}'"
else
	make -C ${DIR}
fi
