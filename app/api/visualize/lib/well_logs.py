import matplotlib.pyplot as plt
import random
import lasio
from io import BytesIO
from app.api.utils.models import FileDB

def generate_well_logs(file: FileDB):

    log = lasio.read(file.file_location)

    df = log.df()
    n_curves = len(log.curves)-1
    fig, axes = plt.subplots(nrows=1, ncols=n_curves, figsize=(10+(n_curves*2), 20))
    for i, curve in enumerate(log.curves[1:]):
        ax = axes[i]
        ax.plot(df[curve.mnemonic], df.index, color="#{:06x}".format(random.randint(0, 0xFFFFFF)))
        ax.set_xlabel(curve.mnemonic)
        ax.grid()

    axes[0].set_ylabel("Depth")
    plt.tight_layout()
    buf = BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)

    return buf