#include <stdio.h>
typedef struct object{
 int x;
 int y;
 char* z;
}object;
int main(){
 object x;
 x.x=42;
 x.y=13;
 x.z="hello world"; 
 printf("%s",x.z);
 return 0;
}
