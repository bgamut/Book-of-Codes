#include <stdio.h>
#include "print.h"

void print(CALC_DATA data){
	printf("%i%c%i==%i\n",
		data.operand1,
		data.operator,
		data.operand2,
		data.result
	);
}
