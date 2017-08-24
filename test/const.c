#include <stdio.h>
#include <unistd.h>
#include <errno.h>
#include <sys/types.h>

int main()
{
    printf("EINVAL: %d\n", EINVAL);
    printf("EPERM: %d\n", EPERM);
    printf("ESRCH: %d\n", ESRCH);

    return 0;
}

