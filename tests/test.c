#include <stdio.h>
#include <unistd.h>

void foo(int val)
{
    int my_local = val + 2;
    int i;

    printf("addr of my_local: %lld\n", (unsigned long long) &my_local);
    for (i = 0;i < my_local; i++) {
        __asm__ __volatile__("int3");
        sleep(1);
        printf("%d\n", i);
    }

    // while (1) {
    //     sleep(1);
    // }
}

int main()
{
    foo(0);

    return 0;
}
