/*
 */
package jmultithreading;

/**
 *
 */
public class JMultithreading extends Thread {

    private final static int NUM_CORES = 2;
    private final static long NUM_TO_INCREMENTS = 10 * 1000 * 1000 * 1000;

    private static final JMultithreading[] THREADS_ARRAY = new JMultithreading[NUM_CORES];

    private static long x;
    private static long start = 0;

    public static void initAll() {
        for (int i = 0; i < NUM_CORES; i++) {
            THREADS_ARRAY[i] = new JMultithreading("thread_" + Integer.toString(i));
        }
    }

    public static void startAll() {
        System.out.printf("Start time %d ns\n", System.nanoTime());
        for (int i = 0; i < NUM_CORES; i++) {
            THREADS_ARRAY[i].start();
        }
    }

    public static void waitAll() {
        int cnt = NUM_CORES;
        try {
            while (cnt > 0) {
                cnt = 0;
                for (int i = 0; i < NUM_CORES; i++) {
                    if (THREADS_ARRAY[i].t.isAlive()) {
                        cnt++;
                    }
                    if (cnt > 0) {
                        Thread.sleep(1);
                    }
                }
            }
            long duration = System.nanoTime() - start;
            System.out.printf("Execution time: %d\nTime per inc:%d\n", duration, duration / (NUM_TO_INCREMENTS));
        } catch (InterruptedException e) {
            System.out.println("Main thread interrupted");
        }
        long duration = System.nanoTime() - start;
        System.out.println("Main thread run is over");
    }

    public static long get_x() {
        return x;
    }

    public Thread t;
    private final String threadName;

    JMultithreading(String name) {
        threadName = name;
        System.out.println("Creating " + threadName);
    }

    @Override
    public void start() {
        start = 0;
        if (t == null) {
            t = new Thread(this, threadName);
            t.start();
        }
    }

    @Override
    public void run() {
        if (start == 0) {
            start = System.nanoTime();
        }

        for (long i = 0; i < NUM_TO_INCREMENTS; i++) {
            x++;
        }
    }

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        initAll();
        startAll();
        waitAll();
        System.out.printf("x=%d\n", get_x());
        System.out.println("the end");
    }

}
