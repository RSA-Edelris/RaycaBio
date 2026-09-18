
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, Polygon, FancyArrow
from matplotlib.collections import LineCollection
from matplotlib.path import Path
import matplotlib.patheffects as pe
from scipy.interpolate import CubicSpline
import matplotlib.colors as mcolors

def smooth_spline(x, y, n=200):
    """Cubic spline through 2-D points, return n interpolated points."""
    if len(x) < 2:
        return x, y
    t = np.linspace(0, 1, len(x))
    cs_x = CubicSpline(t, x)
    cs_y = CubicSpline(t, y)
    ts = np.linspace(0, 1, n)
    return cs_x(ts), cs_y(ts)

def perp_unit(x, y):
    """Perpendicular unit vector along the spline."""
    dx = np.gradient(x)
    dy = np.gradient(y)
    nrm = np.sqrt(dx**2 + dy**2) + 1e-9
    return -dy/nrm, dx/nrm

def draw_helix(ax, x, y, width=1.6, color='#2ecc71', zorder=3, depth_shade=0):
    """Draw a helix segment as a wide ribbon with sine-wave oscillation."""
    if len(x) < 3:
        ax.plot(x, y, '-', color=color, lw=width*3, solid_capstyle='round',
                zorder=zorder)
        return
    xs, ys = smooth_spline(x, y, n=max(80, len(x)*8))
    px, py = perp_unit(xs, ys)
    # sine-wave oscillation on the ribbon
    t = np.linspace(0, len(x)*1.5*np.pi, len(xs))
    osc = np.sin(t) * (width * 0.55)
    xr = xs + px * osc
    yr = ys + py * osc
    # shade slightly by depth
    shade = max(0, min(1, 0.55 + depth_shade * 0.25))
    c_rgb = np.array(mcolors.to_rgb(color)) * shade
    # wide ribbon border
    ax.plot(xs + px*width, ys + py*width, '-', color=np.clip(c_rgb*0.6,0,1),
            lw=0.6, zorder=zorder-0.1, alpha=0.6)
    ax.plot(xs - px*width, ys - py*width, '-', color=np.clip(c_rgb*0.6,0,1),
            lw=0.6, zorder=zorder-0.1, alpha=0.6)
    # fill ribbon
    xfill = np.concatenate([xs + px*width, (xs - px*width)[::-1]])
    yfill = np.concatenate([ys + py*width, (ys - py*width)[::-1]])
    poly = Polygon(np.column_stack([xfill, yfill]),
                   closed=True, facecolor=color, edgecolor='none',
                   alpha=0.85, zorder=zorder)
    ax.add_patch(poly)
    # sine trace on top
    ax.plot(xr, yr, '-', color=np.clip(c_rgb*1.3,0,1), lw=1.0,
            zorder=zorder+0.1, alpha=0.9)

def draw_strand(ax, x, y, width=1.2, color='#27ae60', zorder=3, depth_shade=0):
    """Draw a beta strand as a flat ribbon ending in an arrowhead."""
    if len(x) < 2:
        return
    xs, ys = smooth_spline(x, y, n=max(60, len(x)*6))
    px, py = perp_unit(xs, ys)
    shade = max(0, min(1, 0.55 + depth_shade * 0.25))
    # body: rectangle ribbon (all but last 20%)
    cut = int(len(xs) * 0.78)
    xb  = np.concatenate([xs[:cut]+px[:cut]*width, (xs[:cut]-px[:cut]*width)[::-1]])
    yb  = np.concatenate([ys[:cut]+py[:cut]*width, (ys[:cut]-py[:cut]*width)[::-1]])
    poly_body = Polygon(np.column_stack([xb, yb]), closed=True,
                        facecolor=color, edgecolor=np.clip(np.array(mcolors.to_rgb(color))*0.6,0,1),
                        linewidth=0.4, alpha=0.9, zorder=zorder)
    ax.add_patch(poly_body)
    # arrowhead: triangle from cut to tip
    tip_x, tip_y = xs[-1], ys[-1]
    aw = width * 2.2
    x_arr = [xs[cut]-px[cut]*aw, xs[cut]+px[cut]*aw, tip_x]
    y_arr = [ys[cut]-py[cut]*aw, ys[cut]+py[cut]*aw, tip_y]
    poly_head = Polygon(np.column_stack([x_arr, y_arr]), closed=True,
                        facecolor=color, edgecolor=np.clip(np.array(mcolors.to_rgb(color))*0.6,0,1),
                        linewidth=0.4, alpha=0.95, zorder=zorder+0.1)
    ax.add_patch(poly_head)

def draw_loop(ax, x, y, lw=1.2, color='#1a9950', zorder=2, depth_shade=0):
    """Draw a loop as a thin smooth line."""
    if len(x) < 2:
        return
    xs, ys = smooth_spline(x, y, n=max(40, len(x)*4))
    shade = max(0, min(1, 0.55 + depth_shade * 0.25))
    c_rgb = np.clip(np.array(mcolors.to_rgb(color)) * shade * 1.3, 0, 1)
    ax.plot(xs, ys, '-', color=c_rgb, lw=lw, solid_capstyle='round',
            zorder=zorder, alpha=0.85)
