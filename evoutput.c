#define _GNU_SOURCE

#include <linux/version.h>
#include <linux/input.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <dirent.h>
#include <string.h>
#include <fcntl.h>

#define DEV_INPUT_EVENT "/dev/input"
#define EVENT_DEV_NAME "event"

static int is_event_device(const struct dirent *dir) {
	return strncmp(EVENT_DEV_NAME, dir->d_name, 5) == 0;
}

void scan_devices(void)
{
	struct dirent **namelist;
	int i, ndev, devnum;
	char *filename;
	int max_device = 0;

	ndev = scandir(DEV_INPUT_EVENT, &namelist, is_event_device, versionsort);

	if (ndev <= 0)
		return NULL;

	fprintf(stderr, "Available devices:\n");

	for (i = 0; i < ndev; i++)
	{
		char fname[64];
		int fd = -1;
		char name[256] = "???";

		snprintf(fname, sizeof(fname),
			 "%s/%s", DEV_INPUT_EVENT, namelist[i]->d_name);
		fd = open(fname, O_RDONLY);
		if (fd < 0)
			continue;
		ioctl(fd, EVIOCGNAME(sizeof(name)), name);

		fprintf(stderr, "%s:	%s\n", fname, name);
		close(fd);

		sscanf(namelist[i]->d_name, "event%d", &devnum);
		if (devnum > max_device)
			max_device = devnum;

		free(namelist[i]);
	}
}

int main()
{
    scan_devices();
}
