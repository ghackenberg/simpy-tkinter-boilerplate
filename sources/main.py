import threading
import tkinter
import simpy
import simpy.rt

FRAMES_PER_SECOND = 30

SIMULATION_DURATION = 10

# Create the GUI window
window = tkinter.Tk()
window.title("SimPy Tkinter Boilerplate")
window.geometry("400x400")

# Create a canvas inside the window
canvas = tkinter.Canvas(window, width=400, height=400)
canvas.pack()

# A simulation task process
def task(env):
    rectangle = canvas.create_rectangle(0, 0, 10, 10, fill='blue')
    while True:
        print('Task.before %d' % env.now)
        yield env.timeout(5)
        print('Task.between %d' % env.now)
        yield env.timeout(2)
        print('Task.after %d' % env.now)
        canvas.move(rectangle, 5, 5)

# A simulation clock process
def clock(env):
    text = canvas.create_text(10, 10, fill='black', anchor='nw', text='Time = %d' % env.now)
    while True:
        print('Clock.tick %d' % env.now)
        yield env.timeout(1)
        canvas.itemconfigure(text, text='Time = %s Seconds' % f"{env.now / FRAMES_PER_SECOND:.{3}f}")

# The simulation thread routine
def run():
    env = simpy.rt.RealtimeEnvironment(factor=1/FRAMES_PER_SECOND, strict=False)
    env.process(task(env))
    env.process(clock(env))
    env.run(until=SIMULATION_DURATION * FRAMES_PER_SECOND + 1)

# Create and start the background simulation thread
thread = threading.Thread(target=run)
thread.start()

# Run GUI event processing and rendering on the main thread
window.mainloop()