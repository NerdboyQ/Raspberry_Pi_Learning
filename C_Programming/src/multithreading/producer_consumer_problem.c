#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <stdbool.h>

#define WORKER_CNT 4
#define MAX_CARS 10

// signals that there is a car vacancy in the car wash line
sem_t cars_avail;
// signals that cars are available to wash
sem_t wash_avail;

// protects critical shared resource logic
pthread_mutex_t mtx_lock;

/**
 * Car Wash Line Data structure
 * works as a circular buffer
 */
typedef struct {
    int capacity, tail, head, count;
    int *cars;
} car_wash_line_t;

// car wash line
car_wash_line_t *cw_line;

/**
 * Initializes a new Car Wash Line data structure
 * 
 * @param cw_line: car wash line pointer to initialize
 * @param capacity: total capacity of cars
 */
void car_wash_init(car_wash_line_t *cw_line, int capacity) {
    cw_line->cars = (int*)calloc(capacity, sizeof(int));
    cw_line->capacity = capacity;
    cw_line->head = 0;
    cw_line->tail = 0;
    cw_line->count = 0;
}

/**
 * Determines if a car wash line is empty
 * 
 * @param cw_line: car wash line to check
 * 
 * @return true if the line is empty
 */
bool car_wash_line_empty (car_wash_line_t *cw_line) { return cw_line->count == 0; };

/**
 * Determines if a car wash line is full
 * 
 * @param cw_line: car wash line to check
 * 
 * @return true if the line is full
 */
bool car_wash_line_full (car_wash_line_t *cw_line) { return cw_line->count == cw_line->capacity; };

/**
 * Enters a car in the car wash line to be washed
 * 
 * @param cw_line: car wash line to update
 * @param car_num: the number for the car entered
 * 
 */
void car_wash_line_enter_car (car_wash_line_t *cw_line, int car_num) {
    cw_line->cars[cw_line->head] = car_num;
    cw_line->head = (cw_line->head+1) % cw_line->capacity;
    
    if (car_wash_line_full(cw_line)) {
        cw_line->tail = (cw_line->tail+1) % cw_line->capacity; 
    } else {
        cw_line->count+=1;
    }
}

/**
 * Takes a car from the car wash line to start washing
 * 
 * @param cw_line: car wash line to check
 * 
 * @return the line number for the car
 */
int car_wash_line_take_car (car_wash_line_t *cw_line) {
    if (car_wash_line_empty(cw_line)) return 0;

    int tmp = cw_line->cars[cw_line->tail];
    cw_line->cars[cw_line->tail] = 0;

    cw_line->tail = (cw_line->tail+1) % cw_line->capacity; 
    cw_line->count-=1;
    return tmp;
}

/**
 *  Prints the current numbers for each car in the line
 * 
 * @param cw_line: car wash line to check
 */
void car_wash_show_line (car_wash_line_t * cw_line) {
    if (car_wash_line_empty(cw_line)) {
        printf("No Cars in the line!\n");
        return;
    }

    for (int i = 0; i < cw_line->count; i++) {
        if (!i) printf("%d", cw_line->cars[(cw_line->tail+i)%cw_line->capacity]);
        else printf("->%d", cw_line->cars[(cw_line->tail+i)%cw_line->capacity]);
    }

    printf("\n");
}

/**
 * Cleans up/Deallocates memory for car wash line
 * 
 * @param cw_line: car wash line to check
 */
void car_wash_line_destroy(car_wash_line_t * cw_line) {
    free(cw_line->cars);
    cw_line->cars = NULL;
}

/**
 * Thread Task to place cars in the car wash line for washing
 */
void *take_car() {
    for (;;) {
        sem_wait(&wash_avail);
        pthread_mutex_lock(&mtx_lock);
        int car_num = (rand() % 100) + 1;
        car_wash_line_enter_car(cw_line, car_num);
        printf("[0x%lx] new car: %d\n", (pthread_self() >> 16) & 0xFFFF, car_num);         
        pthread_mutex_unlock(&mtx_lock);
        sem_post(&cars_avail);
    }

    pthread_exit(NULL);
}

/**
 * Thread Task to take cars from the car wash line to be washed
 */
void *wash_car() {
    for (;;) {
        sem_wait(&cars_avail);
        pthread_mutex_lock(&mtx_lock);
        int car_num = car_wash_line_take_car(cw_line);
        printf("[0x%lx] washing car: %d\n", (pthread_self() >> 16) & 0xFFFF, car_num);            
        pthread_mutex_unlock(&mtx_lock);
        sem_post(&wash_avail);
    }

    pthread_exit(NULL);
}

int main (int argc, char** kwargs) {
    // syntax for semaphore init:
    // sem_init([sem_t ptr], [thread shared: 0, or process shares 1], [initial value])
    sem_init(&wash_avail, 0, 1); // initializes the semaphore with a 1
    sem_init(&cars_avail, 0, 0); // initializes the semaphore with a 0

    // pthread init syntax"
    // pthread_mutex_init([mutex ptr], [mutex attribute])
    pthread_mutex_init(&mtx_lock, NULL);

    pthread_t WORKERS[WORKER_CNT];
    cw_line = (car_wash_line_t*)malloc(sizeof(car_wash_line_t));
    car_wash_init(cw_line, MAX_CARS);
    
    for (int i=0; i< WORKER_CNT;i++) pthread_create(&WORKERS[i], NULL, i % 2 ? wash_car : take_car, NULL);
    

    for (int i=0; i< WORKER_CNT;i++) pthread_join(WORKERS[i], NULL);   
    
    car_wash_line_destroy(cw_line);
    pthread_mutex_destroy(&mtx_lock);
    sem_destroy(&wash_avail);
    sem_destroy(&cars_avail);

    return 0;
}
