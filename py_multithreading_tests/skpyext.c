
#include <stdlib.h>

#define __USE_GNU
#include <sched.h>

#include <pthread.h>
//#include <linux/sched.h>

//#include <iostream>
//#include <stdint.h>
//#include <unistd.h>


//#include <mutex>

unsigned long int get_cur_thread(){
	return pthread_self();
}

int stick_thread_to_core(int core_id) {
    cpu_set_t cpuset;

    CPU_ZERO(&cpuset);
    CPU_SET(core_id, &cpuset);
    pthread_t current_thread = pthread_self();
    return pthread_setaffinity_np(current_thread, sizeof (cpu_set_t), &cpuset);
}

int cpu_rotate() {
    static int num_cores = 8; //sysconf(_SC_NPROCESSORS_ONLN);
    static volatile int cur_cpu = 2;
    //__sync_fetch_and_add(&cur_cpu, 1);
	cur_cpu+=1;
    if (cur_cpu > num_cores)
    	cur_cpu = 3;

    stick_thread_to_core(cur_cpu);
    return cur_cpu;
}

