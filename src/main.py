import tkinter
import simpy
import simpy.rt
import threading

fps = 30
duration = 10

window = tkinter.Tk()
window.title("SimPy Tkinter Boilerplate")
window.geometry("400x400")

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
        canvas.itemconfigure(text, text='Time = %s Seconds' % f"{env.now / fps:.{3}f}")

def run():
    env = simpy.rt.RealtimeEnvironment(factor=1/fps, strict=False)
    env.process(task(env))
    env.process(clock(env))
    env.run(until=duration * fps + 1)

thread = threading.Thread(target=run)
thread.start()

window.mainloop()