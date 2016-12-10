/* example.i */
%module skpyext
%{
/* Put header files here or function declarations like below */
extern unsigned long int get_cur_thread();
extern int stick_thread_to_core(int n);
extern int cpu_rotate();
%}

extern unsigned long int get_cur_thread();
extern int stick_thread_to_core(int n);
extern int cpu_rotate();
