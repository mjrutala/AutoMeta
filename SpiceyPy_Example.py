#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 10:11:09 2023

@author: mrutala
"""

import spiceypy as spice
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt

from make_Metakernel import *

km_to_AU = 1./1.496e8
km_to_RJ = 1./71492.
km_to_RS = 1./58232.

def test_SPICE():
   """
   Print the SPICE toolkit version to test that it was installed correctly
   """
   toolkit_version = spice.tkvrsn("TOOLKIT")
   print('The SPICE toolkit version installed is: ' + toolkit_version)
    
def test_Metakernel():
    """
    Create a Voyager 1 Metakernel in a local directory for future tests
    """
    voy1_mk_filepath = make_Metakernel('Voyager 1')
    print('Voyager 1 Metakernel file written to: ')
    print(str(voy1_mk_filepath))
    
def plot_VoyagerTrajectory():
    """
    Plot the trajectory of Voyager 1, as observed by the Sun (or, technically, 
    the Solar System Barycenter here), in the J2000 Ecliptic frame, and spanning
    the dates specified
    """
    
    #   Let's start the day after Voyager 1's launch, and end today, in 10 day intervals
    startdate = dt.datetime(1977, 9, 6)
    stopdate = dt.datetime.today() # dt.datetime(1985, 10, 26) # 
    dates = np.arange(startdate, stopdate, dt.timedelta(days=10)).astype(dt.datetime)
    
    #   Furnish the Voyager 1 Metakernel we created previously
    #   This can also be done with a context manager as:
    #         'with spice.KernelPool("SPICE/voyager1/metakernel_voyager1.txt"):'
    #   Which alleviates the need to clear the kernels from memory later,
    #   Although what we do here is the classic, non-python way
    spice.furnsh('SPICE/voyager1/metakernel_voyager1.txt')
        
    #   Epoch Times (ets): Barycentric Dynamical Time seconds past J2000 epoch
    #   These are the times SPICE takes as input
    ets = [spice.datetime2et(date) for date in dates]
    
    # =============================================================================
    #   Use the SPK "EZ Reader" to get the state (position and velocity), as 
    #   well as light travel times, given the Spacecraft Integer Code 
    #   (https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/req/naif_ids.html),
    #   the epoch time, the reference frame, the aberration correction, and 
    #   the observer. Here, '-31' could be replaced with 'VOYAGER 1', and 
    #   'SOLAR SYSTEM BARYCENTER' with '0'
    # =============================================================================
    state, ltime = spice.spkezr('-31', ets, 'ECLIPJ2000', 'NONE', 'SOLAR SYSTEM BARYCENTER')
    
    #   As is, state is a list of 6-element-long numpy arrays; this format is a little nicer to work with
    state = np.array(state).T * km_to_AU
    
    #   Plot the spacecraft's orbit in the J2000 Ecliptic frame, as observed by the Sun (technically, Solar System Barycenter)
    fig, ax = plt.subplots(figsize=(8,6))
    
    ax.plot(state[0,:], state[1,:])
    ax.set(aspect=1, xlabel='Heliocentric Distance [AU]', ylabel='Heliocentric Distance [AU]')
    
    #  For context, plot the orbits of the planets
    bodies = {'SUN': 'xkcd:yellow',
              'MERCURY': 'xkcd:pale green',
              'VENUS': 'xkcd:pale purple',
              'EARTH': 'xkcd:pale blue', 
              'MARS': 'xkcd:pale red',
              'JUPITER BARYCENTER': 'xkcd:peach',
              'SATURN BARYCENTER': 'xkcd:gold',
              'URANUS BARYCENTER': 'xkcd:light teal',
              'NEPTUNE BARYCENTER': 'xkcd:cornflower blue',
              'PLUTO BARYCENTER': 'xkcd:terracotta'}
    for body, color in bodies.items():
        body_state, _ = spice.spkpos(body, ets, 'ECLIPJ2000', 'NONE', 'SOLAR SYSTEM BARYCENTER')
        body_state = np.array(body_state).T * km_to_AU
        
        #   Plot both the full orbit as a line, and the position at the end of
        #   the interval (i.e., today, if unchanged) with a circle
        ax.plot(body_state[0,:], body_state[1,:], color=color, linewidth=0.5)
        ax.plot(body_state[0,-1], body_state[1,-1], color=color, marker='o', markersize=4)
     
    plt.show()
    # =========================================================================
    #   IMPORTANT: Clear the kernels when you're done!
    #   Since the kernels are loaded into memory with spice.furnsh(), they
    #   will eat up your computer's memory if loaded then forgotten about
    # =========================================================================
    spice.kclear()

def plot_VoyagerFlybys():
    """
    Plot the trajectory of Voyager 1, as observed by the Sun (or, technically, 
    the Solar System Barycenter here), in the J2000 Ecliptic frame, and spanning
    the dates specified
    """
    
    #   Let's start the day after Voyager 1's launch, and end today, in 10 day intervals
    startdate = dt.datetime(1977, 9, 6)
    stopdate = dt.datetime.today() # dt.datetime(1985, 10, 26) # 
    dates = np.arange(startdate, stopdate, dt.timedelta(days=10)).astype(dt.datetime)
    
    #   Furnish the Voyager 1 Metakernel we created previously
    #   This can also be done with a context manager as:
    #         'with spice.KernelPool("SPICE/voyager1/metakernel_voyager1.txt"):'
    #   Which alleviates the need to clear the kernels from memory later,
    #   Although what we do here is the classic, non-python way
    spice.furnsh('SPICE/voyager1/metakernel_voyager1.txt')
        
    #   Epoch Times (ets): Barycentric Dynamical Time seconds past J2000 epoch
    #   These are the times SPICE takes as input
    ets = [spice.datetime2et(date) for date in dates]
    
    # =============================================================================
    #   Use the SPK "EZ Reader" to get the state (position and velocity), as 
    #   well as light travel times, given the Spacecraft Integer Code 
    #   (https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/req/naif_ids.html),
    #   the epoch time, the reference frame, the aberration correction, and 
    #   the observer. Here, '-31' could be replaced with 'VOYAGER 1', and 
    #   'SOLAR SYSTEM BARYCENTER' with '0'
    # =============================================================================
    state, ltime = spice.spkezr('-31', ets, 'ECLIPJ2000', 'NONE', 'SOLAR SYSTEM BARYCENTER')
    
    #   As is, state is a list of 6-element-long numpy arrays; this format is a little nicer to work with
    state = np.array(state).T * km_to_AU
    
    #   Plot the spacecraft's orbit in the J2000 Ecliptic frame, as observed by the Sun (technically, Solar System Barycenter)
    fig = plt.figure(figsize=(8,6))

    gs = fig.add_gridspec(2,3)
    axs = []
    axs.append(fig.add_subplot(gs[:, 0]))
    axs.append(fig.add_subplot(gs[0, 1]))
    axs.append(fig.add_subplot(gs[0, 2]))
    axs.append(fig.add_subplot(gs[1, 1]))
    axs.append(fig.add_subplot(gs[1, 2]))
    
    axs[0].plot(state[0,:], state[1,:])
    axs[0].set(xlabel='Heliocentric Distance [AU]', ylabel='Heliocentric Distance [AU]')
    
    #  For context, plot the orbits of the planets
    bodies = {'SUN': 'xkcd:yellow',
              'MERCURY': 'xkcd:pale green',
              'VENUS': 'xkcd:pale purple',
              'EARTH': 'xkcd:pale blue', 
              'MARS': 'xkcd:pale red',
              'JUPITER BARYCENTER': 'xkcd:peach',
              'SATURN BARYCENTER': 'xkcd:gold',
              'URANUS BARYCENTER': 'xkcd:light teal',
              'NEPTUNE BARYCENTER': 'xkcd:cornflower blue',
              'PLUTO BARYCENTER': 'xkcd:terracotta'}
    for body, color in bodies.items():
        #   Since we definitely don't care about the velocities of the planets,
        #   we'll uses 'SPK Pos' for the position and light travel times
        body_state, _ = spice.spkpos(body, ets, 'ECLIPJ2000', 'NONE', 'SOLAR SYSTEM BARYCENTER')
        body_state = np.array(body_state).T * km_to_AU
        
        #   Plot both the full orbit as a line, and the position at the end of
        #   the interval (i.e., today, if unchanged) with a circle
        axs[0].plot(body_state[0,:], body_state[1,:], color=color, linewidth=0.5)
        axs[0].plot(body_state[0,-1], body_state[1,-1], color=color, marker='o', markersize=4)
        axs[0].set(aspect=1, xlabel='AU', ylabel='AU')
    # =========================================================================
    #   Now, we're going to plot the Jupiter and Saturn flybys
    #   A note on the IAU_Jupiter, and IAU_Saturn frames:
    #   *All* SPICE frames are right handed, even if the frames in most common
    #   use are left-handed
    # =========================================================================
    #   Jupiter first
    #   We're going to want better time resolution than 10 days, so let's
    #   let's figure out when the spacecraft was near Juptiter    
    rough_state, _ = spice.spkpos('Voyager 1', ets, 'ECLIPJ2000', 'NONE', 'JUPITER BARYCENTER')
    #   Conver to spherical coordinates, so we can get the radial distance (first column after reshaping)
    rough_state_sph = [spice.recsph(rectan) for rectan in rough_state]
    rough_state_sph = np.array(rough_state_sph).T * km_to_RJ
    #   Get the time when we're remotely close to Jupiter, and create new ets every 10 min.
    near_Jupiter_indx = np.where(np.abs(rough_state_sph[0,:]) < 1000)[0]
    ets_Jupiter = np.arange(ets[near_Jupiter_indx[0]], ets[near_Jupiter_indx[-1]], 600.)
    
    bodies = {'VOYAGER 1': 'gray',
              'IO': 'xkcd:red',
              'EUROPA': 'xkcd:orange',
              'GANYMEDE': 'xkcd:yellow',
              'CALLISTO': 'xkcd:green'}
    for body, color in bodies.items():
        state, _ = spice.spkpos(body, ets_Jupiter, 'ECLIPJ2000', 'NONE', 'JUPITER BARYCENTER')
        state = np.array(state).T * km_to_RJ
        axs[1].plot(state[0,:], state[1,:], color=color, linewidth=1)
    axs[1].plot([0], [0], color='xkcd:peach', marker='o', markersize=4)
    axs[1].set(xlim=(-40,40), xlabel=r'$R_J$',
               ylim=(-40,40), ylabel=r'$R_J$',
               aspect=1)
    axs[1].text(0, 45, 'Voyager 1 Jupiter Flyby', 
                horizontalalignment='center', verticalalignment='center')
    
    #   What does the spacecraft position look like relative to Jupiter's rotation?
    state, _ = spice.spkpos('Voyager 1', ets_Jupiter, 'IAU_JUPITER', 'NONE', 'JUPITER BARYCENTER')
    state = np.array(state).T * km_to_RJ
    axs[2].plot(state[0,:], state[1,:], color='gray', linewidth=1)
    axs[2].plot([0], [0], color='xkcd:peach', marker='o', markersize=4)
    axs[2].set(xlim=(-20,20), xlabel=r'$R_J$',
               ylim=(-20,20), ylabel=r'$R_J$',
               aspect=1)
    axs[2].text(0, 23, "Closest approach \n rel. to Jupiter's rotation", 
                horizontalalignment='center', verticalalignment='center')
    
    #   And Saturn, with the same steps to get appropriate ets
    rough_state, _ = spice.spkpos('Voyager 1', ets, 'ECLIPJ2000', 'NONE', 'SATURN BARYCENTER')
    rough_state_sph = [spice.recsph(rectan) for rectan in rough_state]
    rough_state_sph = np.array(rough_state_sph).T * km_to_RS
    near_Saturn_indx = np.where(np.abs(rough_state_sph[0,:]) < 1000)[0]
    ets_Saturn = np.arange(ets[near_Saturn_indx[0]], ets[near_Saturn_indx[-1]], 600.)
    
    bodies = {'VOYAGER 1': 'gray',
              'MIMAS': 'xkcd:red',
              'ENCELADUS': 'xkcd:orange',
              'TETHYS': 'xkcd:yellow',
              'DIONE': 'xkcd:green',
              'RHEA': 'xkcd:blue',
              'TITAN': 'xkcd:indigo',
              'IAPETUS': 'xkcd:violet'}
    for body, color in bodies.items():
        state, _ = spice.spkpos(body, ets_Saturn, 'ECLIPJ2000', 'NONE', 'SATURN BARYCENTER')
        state = np.array(state).T * km_to_RS
        axs[3].plot(state[0,:], state[1,:], color=color, linewidth=1)
    axs[3].plot([0], [0], color='xkcd:gold', marker='o', markersize=4)
    axs[3].set(xlim=(-40,40), xlabel=r'$R_S$',
               ylim=(-40,40), ylabel=r'$R_S$',
               aspect=1)
    axs[3].text(0, 45, 'Voyager 1 Saturn Flyby', 
                horizontalalignment='center', verticalalignment='center')
    
    #   What does the spacecraft position look like relative to Saturn's rotation?
    state, _ = spice.spkpos('Voyager 1', ets_Saturn, 'IAU_SATURN', 'NONE', 'SATURN BARYCENTER')
    state = np.array(state).T * km_to_RS
    axs[4].plot(state[0,:], state[1,:], color='gray', linewidth=1)
    axs[4].plot([0], [0], color='xkcd:gold', marker='o', markersize=4)
    axs[4].set(xlim=(-20,20), xlabel=r'$R_S$',
               ylim=(-20,20), ylabel=r'$R_S$',
               aspect=1)
    axs[4].text(0, 23, "Closest approach \n rel. to Saturn's rotation", 
                horizontalalignment='center', verticalalignment='center')
    
    
    plt.tight_layout()
    plt.show()
    # =========================================================================
    #   IMPORTANT: Clear the kernels when you're done!
    #   Since the kernels are loaded into memory with spice.furnsh(), they
    #   will eat up your computer's memory if loaded then forgotten about
    # =========================================================================
    spice.kclear()