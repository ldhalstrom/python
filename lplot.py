"""PYTHON PLOTTING UTILITIES
Logan Halstrom
07 OCTOBER 2015

DESCRIPTION:  File manipulation, matplotlib plotting and saving.  A subset of
lutil.py simply for plotting.
"""

import subprocess
import os
import re
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
from matplotlib.transforms import Bbox #for getting plot bounding boxes
import numpy as np
from scipy.interpolate import interp1d

def MakeOutputDir(savedir):
    """make results output directory if it does not already exist.
    instring --> directory path from script containing folder
    """
    #split individual directories
    splitstring = savedir.split('/')
    prestring = ''
    for string in splitstring:
        prestring += string + '/'
        try:
            os.mkdir(prestring)
        except Exception:
            pass

def GetParentDir(savename):
    """Get parent directory from path of file"""
    #split individual directories
    splitstring = savename.split('/')
    parent = ''
    #concatenate all dirs except bottommost
    for string in splitstring[:-1]:
        parent += string + '/'
    return parent

def GetFilename(path):
    """Get filename from path of file"""
    parent = GetParentDir(path)
    filename = FindBetween(path, parent)
    return filename

def NoWhitespace(str):
    """Return given string with all whitespace removed"""
    return str.replace(' ', '')

def FindBetween(str, before, after=None):
    """Returns search for characters between 'before' and 'after characters
    If after=None, return everything after 'before'"""
    # value_regex = re.compile('(?<=' + before + ')(?P<value>.*?)(?='
    #                                 + after + ')')
    if after==None:
        match = re.search(before + '(.*)$', str)
        if match != None: return match.group(1)
        else: return 'No Match'
    else:
        match = re.search('(?<=' + before + ')(?P<value>.*?)(?='
                                    + after + ')', str)
        if match != None: return match.group('value')
        else: return 'No Match'


########################################################################
### PLOTTING ###########################################################
########################################################################

xkcdcolors = ["windows blue", "dusty purple", "leaf green", "macaroni and cheese",  "cherry" , "greyish", "charcoal", "salmon pink", "sandstone",      "tangerine",]
xkcdhex =    ['#3778bf',      '#825f87',      '#5ca904',    '#efb435',              '#cf0234', '#a8a495', "#343837" , "#fe7b7c"     , "#c9ae74"  ,      "#ff9408"   ,]
global colors
colors = xkcdhex

def UseSeaborn(palette='deep', ncycle=6):
    """Call to use seaborn plotting package
    palette --> keyword for default color palette
    ncycle  --> number of colors in color palette cycle
    """
    import seaborn as sns
    global sns
    global colors
    #No Background fill, legend font scale, frame on legend
    sns.set(style='whitegrid', font_scale=1, rc={'legend.frameon': True})
    #Mark ticks with border on all four sides (overrides 'whitegrid')
    sns.set_style('ticks')
    #ticks point in
    sns.set_style({"xtick.direction": "in","ytick.direction": "in"})

    # sns.choose_colorbrewer_palette('q')

    #Nice Blue,green,Red
    # sns.set_palette('colorblind')
    if palette == 'xkcd':
        #Nice blue, purple, green
        sns.set_palette(sns.xkcd_palette(xkcdcolors))
    else:
        sns.set_palette(palette, ncycle)
        #Nice blue, green red
        # sns.set_palette('deep')

        # sns.set_palette('Accent_r')
        # sns.set_palette('Set2')
        # sns.set_palette('Spectral_r')
        # sns.set_palette('spectral')

    #FIX INVISIBLE MARKER BUG
    sns.set_context(rc={'lines.markeredgewidth': 0.1})

    colors = sns.color_palette() #Save new color palette to variable

    #CALL MATPLOTLIB DEFAULTS AGAIN, AFTER SEABORN CHANGED THEM
    matplotlib.rcParams.update(params)
    matplotlib.rcParams.update(tickparams) #DONT CALL THIS IF YOU WANT TIGHT TICK SPACING



#################
#PLOT FORMATTING
# Configure figures for production
WIDTH = 495.0  # width of one column
FACTOR = 1.0   # the fraction of the width the figure should occupy
fig_width_pt  = WIDTH * FACTOR

inches_per_pt = 1.0 / 72.27
golden_ratio  = (np.sqrt(5) - 1.0) / 2.0      # because it looks good
fig_width_in  = fig_width_pt * inches_per_pt  # figure width in inches
fig_height_in = fig_width_in * golden_ratio   # figure height in inches
fig_dims      = [fig_width_in, fig_height_in] # fig dims as a list

#Line Styles
mark = 5
minimark = 0.75
line = 1.5

#dot, start, x, tri-line, plus
smallmarkers = ['.', '*', 'd', '1', '+']
bigmarkers = ['o', 'v', 'd', 's', '*', 'D', 'p', '>', 'H', '8']
scattermarkers = ['o', 'v', 'd', 's', 'p']

#GLOBAL INITIAL FONT SIZES
#default font sizes
Ttl = 24
Lbl = 24
Box = 22
Leg = 20
Tck = 18

#big font sizes
Lbl_big = 32
Leg_big = 24
Box_big = 28
Tck_big = 22

#MAKE FONT DICT GLOBAL SO IT CAN BE MADE AND USED IN DIFFERENT FUNCTIONS
global font_ttl, font_lbl, font_box, font_tck, font_leg

def SetFontDictSize(ttl=None, lbl=None, box=None, tck=None, leg=None):
    """Set font size in styling dictionaries.  Global dictionaries to use for
    font styles in all functions.
    To change a single parameter, call function like: SetFontDictSize(lbl=18)
    ttl --> title, lbl --> axis label, box --> textbox,
    tck --> axis tick labels, leg --> legend text
    """
    global font_ttl, font_lbl, font_box, font_tck, font_leg

    #DEFAULT FONT SIZES
    # if ttl == None: ttl = 18
    # if lbl == None: lbl = 18
    # if box == None: box = 12
    # if tck == None: tck = 16
    # if leg == None: leg = 16

    if ttl == None: ttl = Ttl
    if lbl == None: lbl = Lbl
    if box == None: box = Box
    if tck == None: tck = Tck
    if leg == None: leg = Leg

    #Font Styles
    font_ttl = {'family' : 'serif',
                'color'  : 'black',
                'weight' : 'normal',
                'size'   : ttl,
                }
    font_lbl = {'family' : 'serif',
                'color'  : 'black',
                'weight' : 'normal',
                'size'   : lbl,
                }
    font_box = {'family' : 'arial',
                'color'  : 'black',
                'weight' : 'normal',
                'size'   : box,
                }
    font_tck = tck
    font_leg = leg


#INITIAL FONT DICT SETTINGS
SetFontDictSize()

#Textbox Properties
textbox_props = dict(boxstyle='round', facecolor='white', alpha=0.5)


params = {
        # 'backend': 'ps',
        # 'text.latex.preamble': ['\usepackage{gensymb}'],
        'axes.labelsize' : Lbl,
        'axes.titlesize' : Ttl,
        # 'text.fontsize' : Box,
        'font.size' : Box,
        # 'xtick.major.pad' :
        # 'text.usetex': True,
        'figure.figsize': [6,6],
        # 'font.family': 'Helvetica',
        'font.family': 'serif',
        'font.fantasy': 'xkcd',
        'font.sans-serif': 'Helvetica', #default font for font.family=serif
        'font.monospace': 'Courier',
        #AXIS PROPERTIES
        'axes.titlepad'  : 2*6.0, #title spacing from axis
        'axes.grid'      : True,  #grid on plot
        #LEGEND PROPERTIES
        'legend.fontsize'       : Leg,
        'legend.framealpha'     : 0.5,
        'legend.fancybox'       : True,
        'legend.frameon'        : True,
        'legend.numpoints'      : 1,
        'legend.scatterpoints'  : 1,
        'legend.borderpad'      : 0.1,
        'legend.borderaxespad'  : 0.1,
        'legend.handletextpad'  : 0.2,
        'legend.handlelength'   : 1.0,
        'legend.labelspacing'   : 0,
}

tickparams = {
        'xtick.labelsize': Tck,
        'ytick.labelsize': Tck,
}



#UPDATE MATPLOTLIB DEFAULT PREFERENCES
    #These commands are called again in UseSeaborn since Seaborn resets defaults
     #If you want tight tick spacing, don't update tick size default, just do manually
import matplotlib
matplotlib.rcParams.update(params)
matplotlib.rcParams.update(tickparams)


import matplotlib.ticker as ticker




def PlotStart(title, xlbl, ylbl, horzy='vertical', figsize='square',
                ttl=None, lbl=None, tck=None, leg=None, box=None,
                grid=True, rc=True):
    """Begin plot with title and axis labels.  Space title above plot.
    horzy --> vertical or horizontal y axis label
    figsize --> set figure size. None for autosizing, 'tex' for latex
                    formatting, or 2D list for user specification.
    ttl,lbl,tck --> title, label, and axis font sizes
    grid --> show grid
    rc --> use matplotlib rc params default
    """

    # if not rc:
        # #Reset default tick fontsize to get desired tick spacing
        # matplotlib.rcParams.update({'xtick.labelsize': 12,
        #                             'ytick.labelsize': 12,})

    #SET FIGURE SIZE
    if figsize == None:
        #Plot with automatic figure sizing
        fig = plt.figure()
    else:
        if figsize == 'tex':
            #Plot with latex 2-column figure sizing
            figsize = fig_dims
        elif figsize == 'square':
            figsize = [6, 6]
        #Otherwise, plot with user-specificed dimensions (i.e. [width, height])
        fig = plt.figure(figsize=figsize)

    #PLOT FIGURE
    ax = fig.add_subplot(1, 1, 1)

    if rc:
        #USE MATPLOTLIB RC PARAMS SETTINGS
        if title != None:
            plt.title(title)
        plt.xlabel(xlbl)
        plt.ylabel(ylbl)
    else:



        #USE FONT DICT SETTINGS

        #Set font sizes
        if ttl != None or lbl != None or tck != None or leg != None or box != None:
            #Set any given font sizes
            SetFontDictSize(ttl=ttl, lbl=lbl, tck=tck, leg=leg, box=box)
        else:
            #Reset default font dictionaries
            SetFontDictSize()

        if title != None:
            plt.title(title, fontdict=font_ttl)
        plt.xlabel(xlbl, fontdict=font_lbl)
        plt.xticks(fontsize=font_tck)
        plt.ylabel(ylbl, fontdict=font_lbl, rotation=horzy)
        plt.yticks(fontsize=font_tck)

        # #Return Matplotlib Defaults
        # matplotlib.rcParams.update({'xtick.labelsize': Tck,
        #                             'ytick.labelsize': Tck,})

    # #INCREASE TITLE SPACING
    # if title != None:
    #     ttl = ax.title
    #     ttl.set_position([.5, 1.025])
    # ax.xaxis.set_label_coords( .5, -1.025*10 )
    # ax.yaxis.labelpad = 20

    #TURN GRID ON
    if grid:
        ax.grid(True)

    return fig, ax



# def SubPlotStart(shape, figsize='square',
#                 sharex=False, sharey=False,
#                 ttl=None, lbl=None, tck=None, leg=None, box=None,
#                 grid=True, ):
#     """Just like PlotStart, but for subplots. Enter subplot layout in `shape
#     figsize --> set figure size. None for autosizing, 'tex' for latex
#                     formatting, or 2D list for user specification.
#     ttl,lbl,tck --> title, label, and axis font sizes
#     grid --> show grid
#     rc --> use matplotlib rc params default
#     """

#     #SET FIGURE SIZE
#     if figsize == None:
#         #Plot with automatic figure sizing
#         fig, ax = plt.subplots(shape, sharex=sharex, sharey=sharey)
#     else:
#         if figsize == 'tex':
#             #Plot with latex 2-column figure sizing
#             figsize = fig_dims
#         elif figsize == 'square':
#             figsize = [6, 6]
#         #Otherwise, plot with user-specificed dimensions (i.e. [width, height])
#         fig, ax = plt.subplots(shape, sharex=sharex, sharey=sharey, figsize=figsize)

#     else:

#         #USE FONT DICT SETTINGS

#         #Set font sizes
#         if ttl != None or lbl != None or tck != None or leg != None or box != None:
#             #Set any given font sizes
#             SetFontDictSize(ttl=ttl, lbl=lbl, tck=tck, leg=leg, box=box)
#         else:
#             #Reset default font dictionaries
#             SetFontDictSize()

#         if title != None:
#             plt.title(title, fontdict=font_ttl)
#         # plt.xlabel(xlbl, fontdict=font_lbl)
#         plt.xticks(fontsize=font_tck)
#         # plt.ylabel(ylbl, fontdict=font_lbl, rotation=horzy)
#         plt.yticks(fontsize=font_tck)

#         # #Return Matplotlib Defaults
#         # matplotlib.rcParams.update({'xtick.labelsize': Tck,
#         #                             'ytick.labelsize': Tck,})

#     # #INCREASE TITLE SPACING
#     # if title != None:
#     #     ttl = ax.title
#     #     ttl.set_position([.5, 1.025])
#     # # ax.xaxis.set_label_coords( .5, -1.025*10 )
#     # # ax.yaxis.labelpad = 20

#     # #TURN GRID ON
#     # if grid:
#     #     ax.grid(True)

#     return fig, ax

def MakeTwinx(ax, ylbl='', horzy='vertical'):
    """Make separate, secondary y-axis for new variable with label.
    (must later plot data on ax2 for axis ticks an bounds to be set)
    ax    --> original axes object
    ylbl  --> text for new y-axis label
    horzy --> set orientation of y-axis label
    """
    ax2 = ax.twinx()
    ax2.set_ylabel(ylbl, fontdict=font_lbl, rotation=horzy)
    plt.yticks(fontsize=font_tck)
    return ax2

def MakeTwiny(ax, xlbl=''):
    """Make separate, secondary x-axis for new variable with label.
    (must later plot data on ax2 for axis ticks an bounds to be set)
    ax --> original axes object for plot
    xlbl --> new x-axis label
    """
    ax2 = ax.twiny() #get separte x-axis for labeling trajectory Mach
    # ax2.set_xlabel(xlbl) #label new x-axis
    plt.xticks(fontsize=font_tck) #set tick font size
    ax2.set_xlabel(xlbl, fontdict=font_lbl) #label new x-axis
    plt.xticks(fontsize=font_tck) #set tick font size
    return ax2

def YlabelOnTop(ax, ylbl, x=0.0, y=1.01):
    """Place horizontally oriented y-label on top of y-axis.
    x --> relative x coordinate of text label center (0: right of fig, goes <0)
    y --> relative y coordinate of text label center (1: top of fig, goes <0)
    """
    #rotate ylabel
    ax.set_ylabel(ylbl, rotation=0)
    #set new center coordinates of label
    ax.yaxis.set_label_coords(x, y)

    return ax

def RemoveAxisTicks(ax, axis='both'):
    """Remove numbers and grid lines for axis ticks
    Use to declassify sensitive info
    axis --> Which axis to remove ticks ('x', 'y', 'both')
    """
    if axis == 'both' or axis == 'x':
        ax.get_xaxis().set_ticks([])

    if axis == 'both' or axis == 'y':
        ax.get_yaxis().set_ticks([])

    return ax

def RemoveAxisTickLabels(ax, axis='both', prettygrid=True):
    """Remove numbers from axis tick labels, keep ticks and gridlines
    Use to declassify sensitive info
    NOTE: Call after setting axis limits
    axis --> Which axis to remove ticks ('x', 'y', 'both')
    prettygrid --> set axis ticks to square grid if True
    """
    if axis == 'both' or axis == 'x':
        #remove axis tick labels
        ax.set_xticklabels([])

        #space grid lines nicely
        if prettygrid:
            #get current axis limits
            lim = ax.get_xlim()
            #space grid lines with desired number
            ticks = np.linspace(lim[0], lim[1], 6)
            ax.set_xticks(ticks)

    if axis == 'both' or axis == 'y':
        #remove axis tick labels
        ax.set_yticklabels([])

        #space grid lines nicely
        if prettygrid:
            #get current y limits
            lim = ax.get_ylim()
            #space grid lines with desired number
            ticks = np.linspace(lim[0], lim[1], 6)
            ax.set_yticks(ticks)

    return ax

def MakeSecondaryXaxis(ax, xlbl, tickfunc, locs=5):
    """Make an additional x-axis for the data already plotted
    ax       --> original axes object for plot
    xlbl     --> new x-axis label
    tickfunc --> function that calculates tick value, based on location
    locs     --> desired tick locations (fractions between 0 and 1)
                    If integer value given, use as number of ticks
    """
    #SETUP SECONDARY AXIS
    ax2 = MakeTwiny(ax, xlbl)
    #SETUP TICKS ON SECONDARY AXIS
    ax2.set_xlim(ax.get_xlim()) #set same limits as original x-axis
    if type(locs) == int:
        locs = np.linspace(1, locs) #array between 0 and 1 with n=locs
    ax2.set_xticks(locs) #set new ticks to specificed increment
    ax2.set_xticklabels(tickfunc(locs)) #label new ticks

    return ax2

def SecondXaxisSameGrid(ax1, xold, xnew, xlbl='', rot=0):
    """Make a secondary x-axis with the same tick locations as the original
    for a specific second parameter. Tick values are interpolated to match original
    ax1  --> original axis handle
    xold --> x-data used when plotting with ax1
    xnew --> new x-data to be mapped to second x-axis
    xlbl --> optional axis label for new x-axis
    rot  --> angle to rotate new tick labels, default none
    """
    #Make second x-axis
    ax2 = MakeTwiny(ax1, xlbl)
    #Get relative tick locations of first axis
    tcks1, vals1 = GetRelativeTicksX(ax1)
    #interpolate new x-axis values at these locations
    vals2 = interp1d(xold, xnew, fill_value='extrapolate' )(vals1)
    #set new ticks to specificed increment
    ax2.set_xticks(tcks1)
    #label new ticks
    ax2.set_xticklabels(vals2)
    #rotate new ticks, if specified
    for tk in ax2.get_xticklabels():
        tk.set_rotation(rot)
    return ax2

def GetRelativeTicksX(ax):
    """Get relative tick locations for an x-axis, use to match shared axes.
    Use linear interpolation, leave out endpoints if they exceede the data bounds
    Return relative tick locations and corresponding tick values
    """
    #Get bounds of axis values
    axmin, axmax = ax.get_xlim()
    #Get values at each tick
    tickvals = ax.get_xticks()
    #if exterior ticks are outside bounds of data, drop them
    if tickvals[0] < axmin:
        tickvals = tickvals[1:]
    if tickvals[-1] > axmax:
        tickvals = tickvals[:-1]
    #Interopolate relative tick locations for bounds 0 to 1
    relticks = np.interp(tickvals, np.linspace(axmin, axmax), np.linspace(0, 1))
    return relticks, tickvals

    # #old method, wasnt reliable
    # xmin, xmax = ax.get_xlim()
    # ticks = [(tick - xmin)/(xmax - xmin) for tick in ax.get_xticks()]
    # return ticks

def GetRelativeTicksY(ax):
    """Get relative tick locations for an y-axis, use to match shared axes
    """
    xmin, xmax = ax.get_ylim()
    ticks = [(tick - xmin)/(xmax - xmin) for tick in ax.get_yticks()]
    return ticks

def OffsetTicks(ax, whichax='x', offset=1.5):
    """Offset tick labels so that alternating labels are at different distances
    from the axis.
    Makes it easier to differentiate labels that are close together.
    Note: change tick font size with:
        'ax.tick_params(axis='both', labelsize=ticksize)'
    ax --> plot axis object
    whichax --> choose which axis to offset ('x' default, 'y')
    offset --> factor by which tick label offset will be increased
    """
    #GET AXIS TICK OBJECTS
        #(list of objects, one for each tick label)
    if whichax == 'x':
        #get x-axis ticks to offset
        tks = ax.get_xaxis().majorTicks
    else:
        #get y-axis ticks to offset
        tks = ax.get_yaxis().majorTicks

    #get current pad value (shift pads proportinally to this value)
    pad = tks[0].get_pad()

    #shift every other tick closer to axis (starting with 1st tick)
    for i in range(0, len(tks), 2):
        tks[i].set_pad(0.5*pad)
    #shift every other tick further from axis (starting with 2nd tick)
    for i in range(1, len(tks), 2):
        tks[i].set_pad(offset*pad)

    return ax


def ZeroAxis(ax, dir='x'):
    """Set axis lower bound to zero, keep upper bound
    """
    if dir == 'x':
        ax.set_xlim([0, ax.get_xlim()[1]])
    elif dir == 'y':
        ax.set_ylim([0, ax.get_ylim()[1]])

def ZeroAxes(ax):
    """Set both axes lower bound to zero, keep upper bound
    """
    ax.set_xlim([0, ax.get_xlim()[1]])
    ax.set_ylim([0, ax.get_ylim()[1]])

def Plot(ax, x, y, color, label, linestyle='-',
            marker='None', line=1.5, mark=5):
    """Enter 'Default' to keep default value if entering values for later
    variables"""
    return ax.plot(x, y, color=color, label=label, linestyle=linestyle,
                    linewidth=line, marker=marker, markersize=mark)

def ScatPlot(ax, df, X, Y, lbl, clr=colors[0], mkr='o', plottype='mark'):
    """Make a scatter plot using various styling techniques.
    Plot using data in provided dataframe according to provided keys
    ax --> matplotlib axis object
    df --> dataframe with data to plot
    X, Y --> dataframe keys to plot
    lbl --> plot label
    clr --> plot color
    mkr --> plot marker
    plottype --> type of scatter plot ('mark': hollow marker, 'scat': scatter)
    """

    if plottype == 'mark':
        #HOLLOW MARKER PLOT
        ax.plot(df[X], df[Y],
                label=lbl, color=clr,
                linewidth=0,
                marker=mkr, markevery=1,
                markeredgecolor=clr, markeredgewidth=1,
                markerfacecolor="None",
                )

    elif plottype == 'scat':
        #SCATTER PLOT
        ax.scatter(df[X], df[Y], label=lbl,
                    marker=mkr, s=35, facecolor=clr,
                    # alpha=0.5,
                    edgecolor='black')

    return ax

def PlotLegend(ax, loc='best', alpha=0.5, title=None, fontsize=None, outside=None, ncol=1):
    """General legend command.  Use given handles and labels in plot
    commands.  Curved edges, semi-transparent, given title, single markers
    """
    #default fontsize is already font_leg, but this allows unique user input
    if fontsize == None: fontsize = font_leg

    if outside != None:
        #Legend outside plot
        if outside == 'top':
            #legend on top of lpot
            bbox = (0.5,1)
            loc = 'center'
        else:
            #Legend to right of plot
            bbox = (1,0.5)
            loc = 'center left'
        leg = ax.legend(title=title, framealpha=alpha,
                        prop={'size':fontsize},
                        bbox_to_anchor=bbox, loc=loc, ncol=ncol,
                        )
    else:
        leg = ax.legend(loc=loc, title=title, framealpha=alpha, ncol=ncol,
                        # fancybox=True, frameon=True,
                        # numpoints=1, scatterpoints=1,
                        prop={'size':fontsize},
                        # borderpad=0.1, borderaxespad=0.1, handletextpad=0.2,
                        # handlelength=1.0, labelspacing=0
                        )
    return leg

def PlotLegendLabels(ax, handles, labels, loc='best', title=None, alpha=0.5,
                        fontsize=None, outside=None, ncol=1):
    """Plot legend specifying labels.
    Curved edges, semi-transparent, given title, single markers
    """
    if fontsize == None:
        fontsize = font_leg
    if outside != None:
        #Legend outside plot
        if outside == 'top':
            #legend on top of plot
            # bbox = (0.5,1)
            bbox = (0.5,1.1)
            loc = 'center'
        elif outside == 'bottom':
            #legend on top of plot
            bbox = (0.5,-0.1)
            loc = 'center'
        else:
            #Legend to right of plot
            bbox = (1,0.5)
            loc = 'center left'
        leg = ax.legend(handles, labels, title=title, framealpha=alpha,
                        prop={'size':fontsize},
                        bbox_to_anchor=bbox, loc=loc, ncol=ncol,
                        )
    else:
        leg = ax.legend(handles, labels, loc=loc, title=title, ncol=ncol,
                    framealpha=alpha,
                    # fancybox=True, frameon=True,
                    # numpoints=1, scatterpoints=1,
                    prop={'size':fontsize},
                    # borderpad=0.1, borderaxespad=0.1, handletextpad=0.2,
                    # handlelength=1.0, labelspacing=0
                    )


    return leg

def ColorMap(ncolors, colormap='jet'):
    """return array of colors given number of plots and colormap name
    colormaps: jet, brg, Accent, rainbow
    """
    cmap = plt.get_cmap(colormap)
    colors = [cmap(i) for i in np.linspace(0, 1, ncolors)]
    return colors

def PlotContourFill(ax, X, Y, data, Ncontour=100, lmin=None, lmax=None,
                           cmap=plt.cm.viridis):
    """Plot field data as Ncontour contours filled between.
    Optionally limit contour levels to reside between lmin and lmax.
    ax --> matplotlib axis object on which to plot contours
    X,Y --> mesh grid
    data --> data to plot contours of
    Ncontour --> number of contours to plot
    lmax, lmin --> max/min contour value to color
    cmap --> colormap to use
    """
    #SET DEFAULTS
    if lmin == None:
        lmin = data.min()
    if lmax == None:
        lmax = data.max()

    #PLOT CONTOURS
    contours = ax.contourf(X, Y, data, levels=np.linspace(lmin, lmax, Ncontour), cmap=cmap)
    return contours

def SetColormapGrayscale(nplot):
    """For data sets with too many cases to color individually,
    make grayscale colormap
    REQUIREMENTS: must call 'UseSeaborn' before use
    nplot --> number of cases to plot
    """
    global sns
    #Use divergining color map if more cases than xkcd colors
    sns.set_palette('gray', int(nplot * 1.5))
    colors = sns.color_palette()
    return colors

def PlotColorbar(ax, contours, label, pad=25, form=None, horzy='horizontal'):
    """Add a colorbar to a plot that corresponds to the provided contour data.
    ax --> matplotlib axis object on which to plot colorbar
    contours --> contour data previously plotted with 'contour' or 'contourf'
    label --> colobar text label
    pad --> space between colorbar and label
    form --> colorbar number format (e.g. '%.2f' for 2 decimals)
    """
    cb = plt.colorbar(contours, ax=ax, format=form) #add colorbar
    cb.set_label(label, rotation=horzy, labelpad=pad) #label colorbar
    return cb

def GetPlotBbox(ypad=0.5, xpad=0, shft=0.1, offtop=0.5):
    """Get bounding box of a plot. Used for saving figures.
    ypad --> inches to pad left side with
    xpad --> inches to pad bottom with
    shft --> genearl padding for all sides, based on axis label font size
    offtop --> inches to remove from top (when no title)

    for square bbox: ypad=xpad, offtop=0
    """

    fig = plt.gcf()
    size = fig.get_size_inches() #figsize
    #Make bounding box that is same width/height as values in 'size'
    bbox = Bbox.from_bounds(-ypad-shft, -xpad-shft, size[0]+shft, size[1]+shft-offtop)
        #1st two entries are index (in inches) of lower left corner of bbox
        #2nd two entries are width and height (in inches) of bbox

    return bbox

def SavePlot(savename, overwrite=1, trans=False, bbox='tight', pad=0.5):
    """Save file given save path.  Do not save if file exists
    or if variable overwrite is 1
    trans --> tranparent background if True
    bbox --> 'tight' for tight border (best for individual plots)
             'fixed' for fixed-size border (best for plots that need to be same size)
             'fixedsquare' same as 'fixed' but final shape is square, not rect
    pad  --> lower left corner padding for 'fixed' bbox (inches)
    """
    if os.path.isfile(savename):
        if overwrite == 0:
            print('     Overwrite is off')
            return
        else: os.remove(savename)
    #Make figure save directory if it does not exist
    MakeOutputDir(GetParentDir(savename))

    #Pad bbox with this value to accomodate specific axis label fontsize
    shft = 0.1

    if bbox == 'fixedsquare':
        #SAVE WITH FIXED BBOX, AXIS LABELS PADDED, FINAL SHAPE IS SQUARE
        #Make bounding box that is same width/height as values in 'size'
            #pad left and bottom size so axis labels aren't cut off
        bbox = GetPlotBbox(ypad=pad, xpad=pad, shft=shft, offtop=0)

        # fig = plt.gcf()
        # size = fig.get_size_inches() #figsize
        # #Make bounding box that is same width/height as values in 'size'
        #     #pad left and bottom size so axis labels aren't cut off
        # GetPlotBbox(ypad=pad, xpad=pad, shft=shft, offtop=0)
        # # bbox = Bbox.from_bounds(-pad-shft, -pad-shft, size[0]+shft, size[1]+shft)
        # #     #1st two entries are index (in inches) of lower left corner of bbox
        # #     #2nd two entries are width and height (in inches) of bbox
    elif bbox == 'fixed':
        #SAVE WITH FIXED BBOX, AXIS LABELS PADDED, FINAL SHAPE IS RECTANGLE
        #Make bounding box that is same width/height as values in 'size'
            #pad left side so axis labels aren't cut off
            #bottom side is already ok, don't pad to reduce whitespace
            #top is too high, subtrack some height
        bbox = GetPlotBbox(ypad=pad, xpad=0, shft=shft, offtop=0.5)

        # fig = plt.gcf()
        # size = fig.get_size_inches() #figsize
        # #Make bounding box that is same width/height as values in 'size'
        #     #pad left side so axis labels aren't cut off
        #     #bottom side is already ok, don't pad to reduce whitespace
        #     #top is too high, subtrack some height
        # bbox = Bbox.from_bounds(-pad-shft, 0-shft, size[0]+shft, size[1]+shft-0.5)

    plt.savefig(savename, bbox_inches=bbox, transparent=trans)
    # plt.savefig(savename, bbox_inches='tight', transparent=trans)
    # plt.close()

def ShowPlot(showplot=1):
    """Show plot if variable showplot is 1"""
    if showplot == 1:
        plt.show()
    else:
        plt.close()

def GridLines(ax, linestyle='--', color='k', which='major'):
    """Plot grid lines for given axis.
    Default dashed line, blach, major ticks
    (use: 'color = p1.get_color()' to get color of a line 'p1')
    """
    ax.grid(True, which=which, linestyle=linestyle, color=color)

def TextBox(ax, boxtext, x=0.005, y=0.95, fontsize=font_box['size'],
                alpha=0.5, props=None, color=None, relcoord=True,
                vert='top', horz='left'):
    """Add text box.
    (Anchor position is upper left corner of text box)
    relcoord --> Use relative coordinate achor points (0 --> 1) if true,
                    actual x,y coordinates if False
    vert/horz --> vertical and horizontal alignment of box about given point
                    e.g. center/center places box centered on point
                         top/center places box with point on top center
    """
    if props == None:
        #Default textbox properties
        props = dict(boxstyle='round', facecolor='white', alpha=alpha)
    if color != None:
        #Set box fill and edge color if specified
        props['edgecolor'] = color
        props['facecolor'] = color
    if relcoord:
        #Use relative coordinates to anchor textbox
        ax.text(x, y, boxtext, fontsize=fontsize, bbox=props,
                verticalalignment=vert, horizontalalignment=horz,
                transform=ax.transAxes, #makes coordinate relative
                )
    else:
        #Use absolute coordinates to anchor textbox
        ax.text(x, y, boxtext, fontsize=fontsize, bbox=props,
                verticalalignment=vert, horizontalalignment=horz,)


def TightLims(ax, tol=0.0):
    """Return axis limits for tight bounding of data set in ax.
    NOTE: doesn't work for scatter plots.
    ax  --> plot axes to bound
    tol --> whitespace tolerance
    """
    xmin = xmax = ymin = ymax = None
    for line in ax.get_lines():
        data = line.get_data()
        curxmin = min(data[0])
        curxmax = max(data[0])
        curymin = min(data[1])
        curymax = max(data[1])
        if xmin == None or curxmin < xmin:
            xmin = curxmin
        if xmax == None or curxmax > xmax:
            xmax = curxmax
        if ymin == None or curymin < ymin:
            ymin = curymin
        if ymax == None or curymax > ymax:
            ymax = curymax

    xlim = [xmin-tol, xmax+tol]
    ylim = [ymin-tol, ymax+tol]

    return xlim, ylim

def PadBounds(axes, tol=0):
    """Add tolerance to axes bounds to pad with whitespace"""

    xtol = (axes[1] - axes[0]) * tol
    ytol = (axes[3] - axes[2]) * tol
    tols = [-xtol, xtol, -ytol, ytol]
    for i, (x, t) in enumerate(zip(axes,tols)):
        axes[i] += t
    return axes

def XAxisScale(ax, divby=1000, param='Time', unit='s'):
    """Divide all axis values by provided factor to make easier to read
    """
    #Get current ticks
    vals = ax.get_xticks()
    #Scale tick values
    ax.set_xticklabels([x/divby for x in vals])
    #Reset axis label to indicate scaling
    ax.set_xlabel('{} (${}\\times10^{{{}}}$)'.format(param, unit,
                                                -int(np.floor(np.log10(divby)))))
    return ax

def YAxisScale(ax, divby=1000, param='Time', unit='s'):
    """Divide all axis values by provided factor to make easier to read
    """
    #Get current ticks
    vals = ax.get_yticks()
    #Scale tick values
    ax.set_yticklabels([x/divby for x in vals])
    #Reset axis label to indicate scaling
    ax.set_ylabel('{} (${}\\times10^{{{}}}$)'.format(param, unit,
                                                -int(np.floor(np.log10(divby)))))
    return ax

def LineShrinker(i, width=1.5, factor=0.15):
    """Incrementailly decrease the width of lines in a plot so that all can be
    seen, even if coincident. (First line is full size)
    i      --> index of current line, start with 0
    width  --> starting line width
    factor --> fraction to shrink linewidth by with each increment
    """
    return width * (1 - factor * i)

def VectorMark(ax, x, y, nmark, color='k'):
    """Mark line with arrow pointing in direction of x+.
    Show nmark arrows
    """
    n = len(y)
    dm = int(len(y) / nmark)
    # indicies = np.linspace(1, n-2, nmark)
    indicies = [1]
    while indicies[-1]+dm < len(y)-1:
        indicies.append(indicies[-1] + dm)

    for ind in indicies:
        #entries are x, y, dx, dy
        xbase, ybase = x[ind], y[ind]
        dx, dy = x[ind+1] - x[ind], y[ind+1] - y[ind]
        ax.quiver(xbase, ybase, dx, dy ,angles='xy',scale_units='xy',scale=1)

def PlotArrow(ax, x1, y1, x2, y2, label, head1='<', head2='>',
                color='grey', sz=10):
    """Plot an arrow between two given points.  Specify arrowhead type on
    either side (default double-headed arrow).
    ax      --> plot axis object
    x1,y1   --> x,y coordinates of starting point
    x2,y2   --> x,y coordinates of ending point
    label   --> label for legend
    head1,2 --> first and second arrowheads (e.g. '<', '>', 'v', '^')
    color   --> color of arrow
    sz      --> size of arrowheads
    """
    #Plot line connecting two points
    ax.plot([x1, x2], [y1, y2], color=color, label=label)
    ax.plot(x1, y1, color=color, marker=head1, markersize=sz) #1st arrow head
    ax.plot(x2, y2, color=color, marker=head2, markersize=sz) #2nd arrow head
    return ax

def PlotVelProfile(ax, y, u, color='green', narrow=4):
    """Plot velocity profile as y vs y
    y --> non-dim. vetical grid within BL (y/delta)
    u --> non-dim. x-velocity withing BL (u/u_e)
    color --> sting, color of plot
    narrow --> number of points between arrows
    """
    vertlinex = np.zeros(len(y))
    ax.plot(vertlinex, y, color=color, linewidth=line)
    ax.fill_betweenx(y, vertlinex, u, facecolor=color, alpha=0.2)
    wd, ln = 0.03, 0.03
    for i in range(0, len(y), narrow):
        if abs(u[i]) < ln:
            ax.plot([0, u[i]], [y[i], y[i]], color=color, linewidth=line)
        else:
            ax.arrow(0, y[i], u[i]-ln, 0, head_width=wd, head_length=ln,
                fc=color, ec=color, linewidth=line)
    ax.plot(u, y, color=color, linewidth=line)
    ax.axis([min(u), max(u), min(y), max(y)])
    return ax

def PolyFit(x, y, order, n, showplot=0):
    """Polynomial fit xdata vs ydata points
    x --> independent variable data points vector
    y --> dependent variable data points vector
    order --> order of polynomial fit
    n --> number of points in polynomial fit
    showplot --> '1' to show plot of data fit
    Returns:
    function of polynomial fit
    """
    #New independent variable vector:
    xmin, xmax = x[0], x[-1]
    x_poly = np.linspace(xmin, xmax, n)
    fit = np.polyfit(x, y, order)
    polyfit = np.poly1d(fit)
    y_poly = polyfit(x_poly)
    #Plot Poly Fit
    plt.figure()
    plt.title(str(order) + '-Order Polynomial Fit', fontsize=14)
    plt.xlabel('x', fontsize=14)
    plt.ylabel('y', fontsize=14)
    plt.plot(x, y, 'rx', label='Data')
    plt.plot(x_poly, y_poly, 'b', label='Fit')
    plt.legend(loc='best')
    if showplot == 1:
        plt.show()
    return polyfit
