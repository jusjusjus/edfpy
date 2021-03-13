
import numpy as np
import matplotlib.pyplot as plt


def plot_physical_samples(fo, t0, dt):
    ax = None
    X = fo.get_physical_samples(t0, dt)
    plt.figure(figsize=(20, 10))
    for i, (c, x) in enumerate(X.items()):
        ax = plt.subplot(fo.num_channels, 1, 1+i, frameon=False, sharex=ax)
        t = np.linspace(t0, t0+dt, num=x.size)
        plt.plot(t, x, 'k-')
        plt.xticks(fontsize=20)
        plt.setp(ax.get_xticklabels(), visible=False)
        plt.yticks(fontsize=20)
        plt.ylabel(c, fontsize=20)
        plt.grid()
    plt.setp(ax.get_xticklabels(), visible=True)
    plt.xlabel('time (sec.)', fontsize=20)
    plt.xlim(t[0], t[-1])
    plt.tight_layout()
    plt.show()
