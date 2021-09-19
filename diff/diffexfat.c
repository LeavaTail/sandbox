// SPDX-License-Identifier: GPL-2.0
/*
 *  Copyright (C) 2021 LeavaTail
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <getopt.h>
#include <limits.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <fcntl.h>
#include <ctype.h>
#include <mntent.h>
#include <sys/types.h>
#include <sys/stat.h>

#include "exfat.h"
#include "diffexfat.h"

FILE *output;
unsigned int print_level = PRINT_WARNING;
struct exfat_info info;
node_t *bootlist = NULL;
node_t *fatlist = NULL;
node_t *datalist = NULL;

/**
 * Special Option(no short option)
 */
enum
{
	GETOPT_HELP_CHAR = (CHAR_MIN - 2),
	GETOPT_VERSION_CHAR = (CHAR_MIN - 3)
};

/* option data {"long name", needs argument, flags, "short name"} */
static struct option const longopts[] =
{
	{"help", no_argument, NULL, GETOPT_HELP_CHAR},
	{"version", no_argument, NULL, GETOPT_VERSION_CHAR},
	{0,0,0,0}
};

/**
 * usage - print out usage
 */
static void usage(void)
{
	fprintf(stderr, "Usage: %s [OPTION]... FROM_IMAGE TO_IMAGE\n", PROGRAM_NAME);
	fprintf(stderr, "Compare exFAT filesystem image\n");
	fprintf(stderr, "\n");

	fprintf(stderr, "  --help\tDESCRIPTION.\n");
	fprintf(stderr, "  --version\toutput version information and exit.\n");
	fprintf(stderr, "\n");
}

/**
 * version        - print out program version
 * @command_name:   command name
 * @version:        program version
 * @author:         program authoer
 */
static void version(const char *command_name, const char *version, const char *author)
{
	fprintf(stdout, "%s %s\n", command_name, version);
	fprintf(stdout, "\n");
	fprintf(stdout, "Written by %s.\n", author);
}

/**
 * main   - main function
 * @argc:   argument count
 * @argv:   argument vector
 */
int main(int argc, char *argv[])
{
	int i, index;
	int opt;
	int longindex;
	int ret = -EINVAL;
	struct exfat_bootsec boot1;
	struct exfat_bootsec boot2;
	FILE *fp = NULL;
	char cmdline[CMDSIZE] = {0};
	char buffer[CMDSIZE] = {0};
	unsigned long x;

	while ((opt = getopt_long(argc, argv,
					"",
					longopts, &longindex)) != -1) {
		switch (opt) {
			case GETOPT_HELP_CHAR:
				usage();
				exit(EXIT_SUCCESS);
			case GETOPT_VERSION_CHAR:
				version(PROGRAM_NAME, PROGRAM_VERSION, PROGRAM_AUTHOR);
				exit(EXIT_SUCCESS);
			default:
				usage();
				exit(EXIT_FAILURE);
		}
	}

#ifdef EXFAT_DEBUG
	print_level = PRINT_DEBUG;
#endif

	if (optind != argc - 2) {
		usage();
		exit(EXIT_FAILURE);
	}

	output = stdout;
	if (exfat_init_info())
		goto out;

	if ((info.fd = open(argv[optind], O_RDONLY)) < 0) {
		pr_err("open: %s\n", strerror(errno));
		ret = -EIO;
		goto out;
	}

	if (exfat_load_bootsec(&boot1))
		goto out;
	if (exfat_load_bootsec(&boot2))
		goto out;
	if (exfat_store_info(&boot1))
		goto out;
	if (exfat_traverse_root_directory())
		goto out;

	if (memcmp(&boot1, &boot2, info.sector_size)) {
		pr_err("exfat boot sectors are different.\n");
		goto out;
	}

	snprintf(cmdline, CMDSIZE, "/bin/cmp -l %s %s", argv[1], argv[2]);
	if ((fp = popen(cmdline, "r")) == NULL) {
		pr_err("popen %s: %s\n", cmdline, strerror(errno));
		ret = -errno;
		goto out;
	}

	init_node(&bootlist);
	init_node(&fatlist);
	init_node(&datalist);

	while(fgets(buffer, CMDSIZE - 1, fp) != NULL) {
		x = strtoul(buffer, NULL, 0);
		if (x < EXFAT_FAT(boot1)) {
			append_node(&bootlist, x);
		} else if (x < EXFAT_HEAP(boot1)) {
			append_node(&fatlist, x);
		} else {
			append_node(&datalist, x);
		}
	}
	printf("\n");

	pr_msg("===== Boot Region =====\n");
	print_node(bootlist);
	pr_msg("===== FAT Region =====\n");
	print_node(fatlist);
	pr_msg("===== DATA Region =====\n");
	print_node(datalist);

	free_node(&bootlist);
	free_node(&fatlist);
	free_node(&datalist);

	ret = EXIT_SUCCESS;

cmd_close:
	pclose(fp);
out:
	exfat_clean_info();
	return ret;
}
