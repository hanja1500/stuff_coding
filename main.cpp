#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#define MAX 100

int main() {
    int input_size = 0;
    int set_math[100] = {0, };
    printf("max value of deritives : ");
    scanf("%d", &input_size);
    input_size++;

    for (int i = 0; i < input_size; i++) {
        printf("%dth value\n", input_size - i - 1);
        scanf("%d", &set_math[i]);
    }

    printf("original result is : ");

    for (int i = 0; i < input_size; i++) {
        if (i==input_size-1)
            {printf("%d\n", set_math[i]); break;}
        else if (set_math[i]==0)
            {continue;}
        else if (set_math[i]==1)
            {printf("x^%d+ ", input_size - i - 1);}
        else{
            printf("%d x^%d+ ", set_math[i], input_size - i - 1);
        }
    }

    printf("deritive result is : ");

    for (int i = 0; i < input_size - 1; i++) {
        if (i==input_size-2)
            {printf("%d\n", set_math[i]); break;}
        else if (set_math[i]==0)
            {continue;}
        else if (set_math[i]==1)
            {printf("%d x^%d+ ", input_size - i - 1, input_size - i - 2);}
        else{
            printf("%d x^%d+ ", set_math[i] * input_size - i - 1, input_size - i - 2);
        }
    }
}