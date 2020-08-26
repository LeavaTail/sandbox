# debugfatfs
FAT/exFAT file system debugger.

## Table of Contents
- [Description](#Description)
- [Example](#Example)
- [Requirement](#Requirement)
- [Install](#Install)
- [Authors](#Authors)

## Description
FAT/exFAT has filesystem information(e.g. cluster size, root directory cluster index, ...) in first Sector.  
Some users want to obtain these information to confirm filesystem status.  
In addition, Some developer want to create any FAT/exFAT filesystem image. 

debugfatfs can ontain these inforamtion.

 * Main Boot Sector field
 * Cluster raw data
 * Sector raw data
 * Convert any character
 * Create any directory entry (Only interactive mode)
 * Change any FAT entry (Only interactive mode)
 * Change any allocation bitmap (Only interactive mode)

:warning: debugfatfs can write filesystem image. If you don't want, Please add `-r`(read only) option.

## Example
**Command line mode**
```sh
$ sudo debugfatfs -c 4 /dev/sdc1
media-relative sector offset    :      800 (sector)
Offset of the First FAT         :      800 (sector)
Length of FAT table             :     1984 (sector)
Offset of the Cluster Heap      :     1000 (sector)
The number of clusters          :    50496 (cluster)
The first cluster of the root   :        4 (cluster)
Size of exFAT volumes           : 15818752 (sector)
Bytes per sector                :      512 (byte)
Bytes per cluster               :    32768 (byte)
The number of FATs              :        1
The percentage of clusters      :        0 (%)

Read "/" Directory (4 entries).
System Volume Information 新しいフォルダー DIRECTORY NEW_TEXT.TXT
```

**Interactive mode**
```sh
$ sudo debugfatfs -i /dev/sdc1
Welcome to debugfatfs 0.1 (Interactive Mode)

/> ls
-HSD-    32768 2020-08-17 02:39:27 System Volume Information 
---D-    32768 2020-08-17 02:41:06 新しいフォルダー 
---D-    32768 2020-08-17 02:41:10 DIRECTORY 
----A        0 2020-08-17 02:42:18 NEW_TEXT.TXT 

/> cd DIRECTORY
/DIRECTORY> ls

/DIRECTORY> exit
Goodbye!
```

## Requirements
* [autoconf](http://www.gnu.org/software/autoconf/)
* [automake](https://www.gnu.org/software/automake/)
* [libtool](https://www.gnu.org/software/libtool/)
* [help2man](https://www.gnu.org/software/help2man/)
* [make](https://www.gnu.org/software/make/)

## Install
```sh
$ ./script/bootstrap.sh
$ ./configure
$ make
$ make install
```

## Authors
[LeavaTail](https://github.com/LeavaTail)
