//
//  object.c
//  
//
//  Created by Bernard Ahn on 6/20/17.
//
//

#include <stdio.h>
typedef struct{
    int(*someFunction)();
}object;

int anotherFunction(int number){
    return number;
};

object a(){
    object b;
    b.someFunction=&anotherFunction;
    return b;
};

int main()
{
    object c=a();
    printf("Print object function result: %d\n",c.someFunction(23));
    return 0;
};

//Prints "Print object function result: 23"

