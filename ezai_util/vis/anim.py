from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from io import StringIO
from IPython.display import HTML, display, clear_output
import time

def render_frames(frames, figsize=(30,20)):
    if isinstance(frames[0], StringIO):  # textual frame
        for i in range(len(frames)):
            if i>0:
                clear_output()
            print(frames[i].getvalue())
            time.sleep(1)
    else:                               # RGB frame
        fig = plt.figure(figsize=figsize)
        plt.axis('off')

        plot = plt.imshow(frames[0])

        def init():
            pass

        def update(i):
            plot.set_data(frames[i])
            return plot,

        anim = FuncAnimation(
            fig = plt.gcf(),
            func = update,
            frames=len(frames),
            init_func=init,
            interval=20,
            repeat=True,
            repeat_delay=20)
        plt.close(anim._fig)
        display(HTML(anim.to_jshtml()))