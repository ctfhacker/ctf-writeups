#include "sgnet.h"
#include "sgstatd.h"
#include <unistd.h>

//user to drop privileges to
const char *USER = "nobody";
//port to bind and listen on
const unsigned short PORT = 4242;

int child_main(int sd)		//handler for incoming connections
{
	int choice = 0;
	FILE *fp;
	char path[1000];
	char bin[100];

	//printf("New Connection\n");
	//printf("/bin/cat /home/grinch/flag.txt\n");
	//system("/usr/bin/id");

	if (choice != 2) {
		write(sd, "\nWelcome to the SuperGnome Server Status Center!\n", 51);
		write(sd, "Please enter one of the following options:\n\n", 45);
		write(sd, "1 - Analyze hard disk usage\n", 28);
		write(sd, "2 - List open TCP sockets\n", 26);
		write(sd, "3 - Check logged in users\n", 27);
		fflush(stdout);

		recv(sd, &choice, 1, 0);

		switch (choice) {
		case 49:
			fp = popen("/bin/df", "r");
			if (fp == NULL) {
				printf("Failed to run command\n");
				exit(1);
			}
			while (fgets(path, sizeof(path), fp) != NULL) {
				sgnet_writes(sd, path);

			}
			break;

		case 50:
			fp = popen("/bin/netstat -tan", "r");
			if (fp == NULL) {
				printf("Failed to run command\n");
				exit(1);
			}
			while (fgets(path, sizeof(path) - 1, fp) != NULL) {
				sgnet_writes(sd, path);
			}
			break;

		case 51:
			fp = popen("/usr/bin/who", "r");
			if (fp == NULL) {
				printf("Failed to run command\n");
				exit(1);
			}
			while (fgets(path, sizeof(path) - 1, fp) != NULL) {
				sgnet_writes(sd, path);
			}
			break;

		case 88:
			write(sd, "\n\nH", 4);
			usleep(60000);
			write(sd, "i", 1);
			usleep(60000);
			write(sd, "d", 1);
			usleep(60000);
			write(sd, "d", 1);
			usleep(60000);
			write(sd, "e", 1);
			usleep(60000);
			write(sd, "n", 1);
			usleep(60000);
			write(sd, " ", 1);
			usleep(60000);
			write(sd, "c", 1);
			usleep(60000);
			write(sd, "o", 1);
			usleep(60000);
			write(sd, "m", 1);
			usleep(60000);
			write(sd, "m", 1);
			usleep(60000);
			write(sd, "a", 1);
			usleep(60000);
			write(sd, "n", 1);
			usleep(60000);
			write(sd, "d", 1);
			usleep(60000);
			write(sd, " ", 1);
			usleep(60000);
			write(sd, "d", 1);
			usleep(60000);
			write(sd, "e", 1);
			usleep(60000);
			write(sd, "t", 1);
			usleep(60000);
			write(sd, "e", 1);
			usleep(60000);
			write(sd, "c", 1);
			usleep(60000);
			write(sd, "t", 1);
			usleep(60000);
			write(sd, "e", 1);
			usleep(60000);
			write(sd, "d", 1);
			usleep(60000);
			write(sd, "!\n\n", 4);
			usleep(60000);
			write(sd, "Enter a short message to share with GnomeNet (please allow 10 seconds) => ", 75);
			fflush(stdin);
			sgstatd(sd);

			sgnet_writes(sd, "\nRequest Completed!\n\n");
			break;

		default:
			write(sd, "Invalid choice!\n", 17);
			break;

		}
		shutdown(sd, SHUT_WR);
	}
	return 0;
}

int sgnet_exit()
{
	printf("Canary not repaired.\n");
	exit(0);
}

int sgstatd(sd)
{
	__asm__("movl $0xe4ffffe4, -4(%ebp)");
	//Canary pushed

	char bin[100];
	write(sd, "\nThis function is protected!\n", 30);
	fflush(stdin);
	//recv(sd, &bin, 200, 0);
	sgnet_readn(sd, &bin, 200);
	__asm__("movl -4(%ebp), %edx\n\t" "xor $0xe4ffffe4, %edx\n\t"	// Canary checked
		"jne sgnet_exit");
	return 0;

}

int main(int argc, char **argv)	//main function
{
	(void)argc;
	(void)argv;
	printf("Server started...\n");
	int sd;
	//socket descriptor
	sd = sgnet_listen(PORT, IPPROTO_TCP, NULL);
	sgnet_server(sd, USER, child_main);
	return 0;
}
