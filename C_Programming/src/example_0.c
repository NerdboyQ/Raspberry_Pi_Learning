#include <stdio.h>

float get_sum(float a,float b);
float get_difference(float a, float b);
float get_quotient(float a, float b);
float get_product(float a,float b);


struct Car {
   char nickname[40];
   int year;
   char make[40];
   char model[40];
   char color[40];
};

int main(){
   float a,b;
   printf("--------------------------------------------------------------------\n");
   printf("Hello World, the first example will require two values: A & B:\n\n");
   printf("Please provide a number to use for the a value: ");
   scanf("%f", &a);
   printf("Please provide a number to use for the b value: ");
   scanf("%f", &b);

   printf("The values that will be considered will be a: %.2f, and b: %.2f\n\n", a,b);
   float sum = get_sum(a,b);
   float difference = get_difference(a,b);
   float product = get_product(a,b);
   float quotient = get_quotient(a,b);

   printf("The sum of the two values is:\t%.2f.\n",sum);
   printf("The difference of the two values is:\t%.2f.\n",difference);
   printf("The product of the two values is:\t%.2f.\n",product);
   printf("The quotient of the two values is:\t%.2f.\n",quotient);
   
   printf("--------------------------------------------------------------------\n");
   struct Car bucket,nada,kit,tonka,ebony;
   strcpy(bucket.nickname,"bucket");
   strcpy(bucket.make, "Mercury");
   strcpy(bucket.model, "Grand Marquis");
   strcpy(bucket.color, "Forest Green");
   bucket.year = 1996;

   strcpy(kit.nickname, "kit");
   strcpy(kit.make, "Toyota");
   strcpy(kit.model, "Celica GT");
   strcpy(kit.color, "White");
   kit.year = 1992;

   strcpy(nada.nickname,"nada");
   strcpy(nada.make, "Chevrolet");
   strcpy(nada.model, "Cavalier");
   strcpy(nada.color, "Green");
   nada.year = 1996;

   strcpy(tonka.nickname,"tonka");
   strcpy(tonka.make, "Ford");
   strcpy(tonka.model, "Explorer Sport Trac");
   strcpy(tonka.color,"White");
   tonka.year = 2001;

   strcpy(ebony.nickname, "ebony");
   strcpy(ebony.make, "Chevrolet");
   strcpy(ebony.model, "Malibu LS");
   strcpy(ebony.color, "Black");
   ebony.year = 2012;

   struct Car car_lot[5];
   car_lot[0] = bucket;
   car_lot[1] = kit;
   car_lot[2] = nada;
   car_lot[3] = tonka;
   car_lot[4] = ebony;
   printf("The lines below will show an example of a struct and an array:\n\n");
   for(int i = 0;i<5;i++){
      printf("The car I called %s was a %s %d %s %s.\n",car_lot[i].nickname, car_lot[i].color, car_lot[i].year,car_lot[i].make, car_lot[i].model);
   }

   
   return 0;
}

float get_sum(float a, float b){
   return (a+b);
}

float get_difference(float a, float b){
   return (a-b);	
}

float get_product(float a, float b){
   return (a*b);
}

float get_quotient(float a, float b){
   return (a/b);
}
