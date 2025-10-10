#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <stdbool.h>
#include <pthread.h>

#define MAX_WEIGHT 850
#define MAX_PASSENGERS 12

/**
 * Passenger Structure
 */
typedef struct { int weight; } passenger_t;

/**
 * Elevator Structure
 */
typedef struct {
    int weight_limit, max_passengers;
    passenger_t *passengers;
    int curr_weight, curr_occupancy;
    uint8_t head, tail;
    // concurrency safe params
    pthread_mutex_t mutex_elev_access; // Mutext for elevator lock access
    
    pthread_cond_t cond_elev_not_full; // Condition Variable to signal that the elevator is not full
    pthread_cond_t cond_elev_has_passengers; // Condition Variable to signal that the elevator has passengers
} elev_t;

// shared elevator 
elev_t elevator;

/**
 * Initializes elevator 
 *
 * @param elev: elevator to initialize
 *
 * @return true is elevator successfully initialized
 *
 */
bool elevator_init(elev_t *elev) {
    elev->weight_limit = MAX_WEIGHT;
    elev->max_passengers = MAX_PASSENGERS;
    
    elev->curr_weight = 0;
    elev->curr_occupancy = 0;
    
    elev->head = 0;
    elev->tail = 0;
    
    elev->passengers = (passenger_t*)malloc(sizeof(passenger_t) * MAX_PASSENGERS);
    
    // if allocation fails
    if (!elev->passengers) return false;
    
    // initialize mutex lock
    pthread_mutex_init(&elev->mutex_elev_access, NULL);
    
    // initialize both conditional signals
    pthread_cond_init(&elev->cond_elev_not_full, NULL);
    pthread_cond_init(&elev->cond_elev_has_passengers, NULL);
    
    return true;
}

/**
 * Verifies if an elevator is at maximum occupancy
 *
 * @param elev: elevator
 *
 * return true if elevator is at maximum occupancy 
 */
bool elevator_full (elev_t *elev) { return elev->curr_occupancy == elev->max_passengers; }

/**
 * Verifies if an elevator is empty
 *
 * @param elev: elevator
 *
 * return true if elevator is empty 
 */
bool elevator_empty (elev_t *elev) { return !elev->curr_occupancy; }

/**
 * Deallocates memory for elevator & destroys synchronization mechanisms
 *
 * @param elev: elevator
 */
void elevator_destroy (elev_t *elev) {
    free(elev->passengers);
    pthread_cond_destroy(&elev->cond_elev_has_passengers);
    pthread_cond_destroy(&elev->cond_elev_not_full);
    pthread_mutex_destroy(&elev->mutex_elev_access);
    
    printf("Cleaned up the memory for the elevator.\n");
}

/**
 * Thread target to accept passengers on the elevator 
 *
 */
void *permit_passenger(void *arg) {
    for (int i =0; i< 20; i++){
        pthread_mutex_lock(&elevator.mutex_elev_access);
        
        // if the elevator is full wait until it is no longer full
        while (elevator_full(&elevator)) {
            printf("The elevator is full!\n");
            // make thread wait for full condition signal
            pthread_cond_wait(&elevator.cond_elev_not_full, &elevator.mutex_elev_access);
        }
        
        printf("There is vacancy for a person to be permitted\n");
        // randomly generate 1 or more passengers to add to simulate passengers
        // walking onto the elevator 
        int n = 1 + rand() % (elevator.max_passengers - elevator.curr_occupancy);
        
        for (int i =0; i < n; i++) {
            passenger_t pass = {50 + rand() % 160};
            
            // of the passenger adds too much weight, which exceeds that max weight limit
            // do not allow the passenger onto the elevator 
            if (pass.weight + elevator.curr_weight > elevator.weight_limit) printf("!!This person is too heavy to be safely permitted onto the elevator.\n");
            else {
                *(elevator.passengers+elevator.tail) = pass;
                printf(" + A passenger %d, weighing %dlbs was permitted\n", elevator.tail ,pass.weight);
                elevator.tail = (elevator.tail + 1) % elevator.max_passengers;
                elevator.curr_weight+=pass.weight;
                elevator.curr_occupancy+=1;
                
                if (elevator.curr_occupancy == elevator.max_passengers) {
                    printf("! The elevator has reached maximum occupancy! ");
                    break; // break loop when limit is met
                }
                
                // check if weight limit met
                if (elevator.curr_weight == elevator.weight_limit) {
                    printf("! The elevator has reached maximum weight! ");
                    break; // break loop when limit is met
                }
            }
        }
        
        // once passengers have been added set the signal for available passengers 
        pthread_cond_signal(&elevator.cond_elev_has_passengers);
        pthread_mutex_unlock(&elevator.mutex_elev_access);
        
        usleep(500000); // sleep for 500ms
    }
    pthread_exit(NULL);
}

/**
 * Thread target to remove passengers from the elevator 
 *
 */
void *release_passenger(void *arg) {
    for (int i =0; i< 20; i++){
        pthread_mutex_lock(&elevator.mutex_elev_access);
        
        // if the elevator is empty, wait until passengers are available to release
        while (elevator_empty(&elevator)) {
            printf("The elevator is empty!\n");
            pthread_cond_wait(&elevator.cond_elev_has_passengers, &elevator.mutex_elev_access);
        }
        
        // randomly generate 1 or more passengers to remove to simulate passengers
        // leaving the elevator 
        int n = 1 + (rand() % (elevator.curr_occupancy));
        for (int i = 0; i < n; i++) {
            int pass_i = (elevator.head + i) % elevator.max_passengers;
            passenger_t pass = *(elevator.passengers+pass_i);
            printf(" - releasing passenger at idx: %d (%dlbs)\n", pass_i, pass.weight);
            elevator.passengers[pass_i].weight = 0;
            elevator.curr_weight-=pass.weight;
        }
        
        elevator.head = (elevator.head + n) % elevator.max_passengers;
        elevator.curr_occupancy-=n;
        
        if (!elevator.curr_occupancy) {
            printf("! the elevator is empty!\n");
            // pthread_cond_signal(&elevator.cond_elev_is_empty);
        }
        
        pthread_cond_signal(&elevator.cond_elev_not_full);
        pthread_mutex_unlock(&elevator.mutex_elev_access);
        usleep(500000);
    }
    pthread_exit(NULL);
}

int main()
{
    pthread_t th0, th1;
    
    if (!elevator_init(&elevator)) {
        printf("There was an error attempting to initialize the elevator.");
        exit(EXIT_FAILURE);
    }
    
    pthread_create(&th0, NULL, permit_passenger, NULL);
    pthread_create(&th1, NULL, release_passenger, NULL);

    
    pthread_join(th0, NULL);
    pthread_join(th1, NULL);
    
    elevator_destroy(&elevator);

    return 0;
}
