from RadarFactory import radar_factory
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib import font_manager
import seaborn as sns
import numpy as np

path = './assets/fonts/Montserrat-Regular.ttf'
font_prop = font_manager.FontProperties(fname=path)


def barGraph_labels(label_type="PlotLabels"):
    if label_type == "PlotLabels":
        bgLabels = [
            "Expected Performance \non Impact Targets",
            "Assessment of \nImpact Dimensions", "Aggregate Impact Rating",
            "Impact Monetization"
        ]
    elif label_type == "IndicatorLabels":
        bgLabels = [["Expected Performance", "on Impact Targets"],
                    ["Assessment of", "Impact Dimensions"],
                    ["Aggregate Impact", "Rating"], ["Impact", "Monetization"]]
    else:
        bgLabels = [["Expected Performance on Impact Targets"],
                    ["Assessment of Impact Dimensions"],
                    ["Aggregate Impact Rating"], ["Impact Monetization"]]
    return bgLabels


def plot_map(data):
    N = len(data[0])
    theta = radar_factory(N, frame='circle')
    spoke_labels = data.pop(0)
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(projection='radar'))
    fig.subplots_adjust(top=1, bottom=0.05)
    colors = ['#354479', '#80b462', '#a74030']
    z = 3
    for d, i, color in zip(data[0][1], range(4), colors):
        aph = 0.25
        i += 1
        if i == 1:
            aph = 0.65
        else:
            aph = 0.55
        if i < 4:
            ax.plot(theta, d, color=color, alpha=aph, zorder=z)
            ax.fill(theta, d, facecolor=color, alpha=aph, zorder=z)
            ax.set_varlabels(spoke_labels)
        z -= 1
    ax.set_rmax(4)
    ax.set_rgrids([0, 1, 2, 3, 4], ['  0', '  1', '  2', '  3', '  4'],
                  angle=67.5,
                  fontproperties=font_prop)
    # If you want labels
    '''labels = (title, 'Median', 'Median (DFI)')
    legend = fig.legend(labels, loc=(0.70, 0.90),
                        labelspacing=0.1, fontsize='small')'''
    filename = './assets/temp/front-map.png'
    fig.savefig(filename, dpi=300, transparent=True)
    plt.close('all')
    return filename


def plot_barGraph(pg_name, peerGrpData, allVerifData):
    sns.set_context("notebook")
    fig, ax = plt.subplots(figsize=(12, 8))
    x = np.arange(4)
    bwid = 0.4
    b1 = ax.bar(x, peerGrpData, width=bwid, label=pg_name, color='#100c6e')
    b2 = ax.bar(x + bwid,
                allVerifData,
                width=bwid,
                label="All Verification Clients",
                color='#2b16b9')
    ax.set_xticks(x + bwid / 2)
    ax.set_xticklabels(barGraph_labels(),
                       fontsize=11,
                       fontproperties=font_prop)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontproperties(font_prop)
    ax.legend(prop=font_prop)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#DDDDDD')
    ax.tick_params(bottom=False, left=False)
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color='#EEEEEE')
    ax.xaxis.grid(False)
    ax.set_ylabel('Percentage of Verified Investors',
                  labelpad=15,
                  fontweight='demi',
                  fontproperties=font_prop)
    fig.tight_layout()
    for bar in ax.patches:
        bar_value = bar.get_height()
        text = f'{bar_value:.0f}%\n'
        text_x = bar.get_x() + bar.get_width() / 2
        text_y = bar.get_y() + bar_value
        bar_color = bar.get_facecolor()
        ax.text(text_x,
                text_y,
                text,
                ha='center',
                va='bottom',
                color=bar_color,
                size=12,
                fontproperties=font_prop)
    img_file = "./assets/temp/pc_bar_graph.png"
    plt.savefig(img_file,
                dpi=300,
                transparent=True,
                pad_inches=0,
                bbox_inches='tight')
    plt.close('all')
    return img_file


def info_graph(y, num1):
    z = 100 - y
    sizes = [y, z]
    colors = ['#032953', '#e2e2e2']
    explode = (0, 0)  # explode a slice if required
    plt.pie(sizes,
            explode=explode,
            startangle=90,
            counterclock=False,
            colors=colors)
    # draw a circle at the center of pie to make it look like a donut
    centre_circle = plt.Circle((0, 0),
                               0.75,
                               color='white',
                               fc='white',
                               linewidth=1.25)
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    # Text
    plt.text(0,
             -0.20,
             f'{y}%',
             ha='center',
             font_properties=font_prop,
             fontsize=85)
    # Set aspect ratio to be equal so that pie is drawn as a circle.
    plt.axis('equal')
    plt.gca().set_axis_off()
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    plt.margins(0, 0)
    img_file = "./assets/temp/pcig_{0}.png".format(num1)
    plt.savefig(img_file, transparent=True, pad_inches=0, bbox_inches='tight')
    plt.close('all')
    return img_file
