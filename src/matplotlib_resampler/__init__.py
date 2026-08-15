import numpy as np
import matplotlib.pyplot as plt
from tsdownsample import MinMaxLTTBDownsampler


class DynamicDownsampler:
    def __init__(self, plt_obj, n_out=2000):
        # This is meant to create a strong reference to prevent being dropped after initialization if we call the
        # wrapper and let it go without using it ever again, the garbage collector will come and remove it. So we
        # attach the instantiation to something that will stay alive the whole time we basically attach our
        # instantiation to a tether we made to the plot object, because the plot object is guaranteed to live the
        # whole time. If you remove this line, you will notice that the downsampling only happens once give it a shot!
        plt_obj._life_tether = self

        # The maximum amount of points you are willing to render at one time
        self.n_out = n_out
        # The plot is embedded into the figure
        fig = plt_obj.gcf()

        self.ds = MinMaxLTTBDownsampler()
        self.data = {}

        # Separate every piece of continuous data to its root properties. x-data, y-data, and a subplot it's on
        for ax in fig.get_axes():
            for line in ax.get_lines():
                x, y = np.asarray(line.get_xdata()), np.asarray(line.get_ydata())

                # Every piece of continuous data drawn has an x, y and subplot it belongs to
                self.data[line] = (x, y, ax)

                # Very first plot samples for when figure renders IF the original plot has more samples than we are
                # willing to render
                if len(y) > n_out:
                    idx = self.ds.downsample(y, n_out=n_out)
                    line.set_data(x[idx], y[idx])

            # Main simple idea. On the GUI event that a zoom or pan occurs, we apply MinMaxLTTB
            ax.callbacks.connect("xlim_changed", self._on_xlim_changed)

        # Redraw
        plt_obj.gcf().canvas.draw_idle()

    # Will be called every xlimit changed event
    def _on_xlim_changed(self, ax):
        # ax.get_xlim() returns the data values, and not the indicies they are in the array.
        # We will have to find where they are in the array
        xlim = ax.get_xlim()

        for line, (x, y, line_ax) in self.data.items():
            # Skip the lines on the subplots we have not zoomed in on. Will have to test on case of sharex=True...
            # IDK we'll see lol
            if line_ax != ax:
                continue

            # We were returned the new x limits in data, not indicies. So where are they in the array?
            s, e = np.searchsorted(x, xlim)

            # We slice the new range in the array to plot
            x_sub, y_sub = x[s:e], y[s:e]

            # Only resample if we are bigger than the max amount the user is willing to plot ont he screen
            if len(y_sub) > self.n_out:
                idx = self.ds.downsample(y_sub, n_out=self.n_out)
                line.set_data(x_sub[idx], y_sub[idx])
            else:
                line.set_data(x_sub, y_sub)

        # Redraw
        ax.figure.canvas.draw_idle()
