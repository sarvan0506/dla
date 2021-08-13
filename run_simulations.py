from dla_sim_normal import DLA_Sim
import threading

folder = './test/'
stickiness = [0.25, 0.85, 0.0075]  # np.linspace(1, 10, 10)
size = 251; particles=15000

def run(size, particles, i):
    print("Running for stickiness", i)
    dla = DLA_Sim(size, i, folder)
    dla.addPoint(particles)
    dla.plot()
    
    print("Done for stickiness", i)

if __name__ == "__main__":

    print("Experiment for size", size, "and particles", particles)
    
    for i in :
        threading.Thread(target=run, args=(size, particles, i,)).start()