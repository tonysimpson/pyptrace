#include <stdio.h>
#include <unistd.h>

void foo()
{
    while (1) {
        printf("hello world\n");
        sleep(1);
    }
}

int main()
{
    foo();

    return 0;
}
