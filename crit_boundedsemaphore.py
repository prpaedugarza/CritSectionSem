from multiprocessing import Value, Array
from multiprocessing import BoundedSemaphore, Process

N = 8

def task(common, tid, critical, semaphore):    
    a = 0
    for i in range(100):
        print(f'{tid}-{i}: Non-critical Section')        
        a += 1
        print(f'{tid}-{i}: End of non-critical Section') 
        semaphore.acquire()
        try:    
            print(f'{tid}-{i}: Critical section')        
            v = common.value + 1
            print(f'{tid}-{i}: Inside critical section')        
            common.value = v
            print(f'{tid}-{i}: End of critical section')        
            critical[tid] = 0   
        finally:
            semaphore.release()

def main():    
    semaphore = BoundedSemaphore()
    lp = []    
    common = Value('i', 0)    
    critical = Array('i', [0]*N)

    for tid in range(N):        
        lp.append(Process(target=task, args=(common, tid, critical, semaphore)))
    print (f"Valor inicial del contador {common.value}")

    for p in lp:        
        p.start()

    for p in lp:        
        p.join()
        
    print (f"Valor final del contador {common.value}")
    print ("fin")


if __name__ == "__main__":    
    main()