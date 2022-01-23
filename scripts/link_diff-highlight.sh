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

function package_manager() {
	if (type "dpkg" > /dev/null 2>&1); then
		MANAGER="dpkg -L"
	elif (type "rpm" > /dev/null 2>&1); then
		MANAGER="rpm -ql"
	else
		echo "None"
	fi
}

if (type ${TARGET} > /dev/null 2>&1); then
	exit 0;
fi

package_manager

if [ ! -z "$MANAGER" ]; then
	ARRAY=($(${MANAGER} git | grep "/${TARGET}$"))
	echo ${ARRAY}
fi

if [ -z ${ARRAY} ]; then
	echo "WARN: ${TARGET} is not installed." 1>&2
	exit 1
fi

for f in ${ARRAY[@]}; do
	if [ -f ${f} ] && [ -x ${f} ]; then
		ln -s ${f} ${OUT}
	fi
done
