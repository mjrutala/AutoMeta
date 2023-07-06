#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Wed Jun 14 15:17:29 2023

@author: mrutala
'''

import subprocess
import os
import glob

import pandas as pd
    
from pathlib import Path



def deprecated_generate_JunoMetakernel(update_files = False):
    import subprocess
    import os
    import glob
    
    output_file = '/Users/mrutala/SPICE/juno/metakernel_juno.txt'
    
    filepattern = '*juno_rec_??????_??????_??????*'
    #filetype = ['.bsp', '.lbl']
    
    destination_dir = '/Users/mrutala/SPICE/juno/kernels/spk/'
    
    command = ['wget']
    flags = ['-r', '-R', '*.html', '-np', '--directory-prefix=' + destination_dir, '-nv', '-nH', '--cut-dirs=8', '--show-progress', '-q']
    filepattern_flags = ['--accept=' + filepattern]
    host_url = ['https://naif.jpl.nasa.gov/pub/naif/pds/data/jno-j_e_ss-spice-6-v1.0/jnosp_1000/data/spk/']
    
    line = command + flags + filepattern_flags + host_url
    if update_files:
        subprocess.run(line)
    
    #  Now that you downloaded all the received Juno telemetry from the front-facing NAIF database
    #  Read the file names and construct a metakernel
    

    metakernel_header = ["# The meta kernel file contains entries pointing to the following SPICE kernels, which the user needs to download.",
                         "#",
                         "#   The following is the contents of a metakernel that was saved with",
                         "#   the name 'metakernel_juno.txt'.",
                         "\\begindata",
                         "    PATH_VALUES = (",
                         "        '/Users/mrutala/SPICE/juno/kernels/',",
                         "        '/Users/mrutala/SPICE/generic/kernels/'",
                         "        )",
                         "    PATH_SYMBOLS = (",
                         "        'SPACECRAFT',",
                         "        'GENERIC'",
                         "        )",
                         "    KERNELS_TO_LOAD = (",
                         "        '$GENERIC/lsk/latest_leapseconds.tls'"]
    metakernel_footer = ["        )",
                         "\\begintext"]


    # =============================================================================
    # Format spacecraft telemetry files for printing
    # =============================================================================
    SPACECRAFT_KERNELS_TO_LOAD = []
    
    sc_rec_tel_long = glob.glob(destination_dir + 'juno_rec_orbit' + '.bsp')
    sc_rec_tel_long_filenames = [os.path.basename(f) for f in sc_rec_tel_long]
    sc_rec_tel_long_filenames.sort()
    sc_rec_tel_long_filenames_formatted = ['\t' + "'$SPACECRAFT" + os.sep + 'spk' + os.sep + filename + "'" for filename in sc_rec_tel_long_filenames]
    
    SPACECRAFT_KERNELS_TO_LOAD.extend(sc_rec_tel_long_filenames_formatted)
    
    sc_rec_tel_short = glob.glob(destination_dir + filepattern[:-1] + '.bsp')
    sc_rec_tel_short_filenames = [os.path.basename(f) for f in sc_rec_tel_short]
    sc_rec_tel_short_filenames.sort()
    sc_rec_tel_short_filenames_formatted = ['\t' + "'$SPACECRAFT" + os.sep + 'spk' + os.sep + filename + "'" for filename in sc_rec_tel_short_filenames]
    
    SPACECRAFT_KERNELS_TO_LOAD.extend(sc_rec_tel_short_filenames_formatted)
    
    check = 'n'
    if os.path.exists(output_file):
        print('Metakernel text file: ' + output_file + 'already exists.')
        check = input('Would you like to overwrite it? (y/n)  ')
    else:
        check = 'y'
    
    if check == 'y':
        with open(output_file, mode='w') as f:
            for output_line in metakernel_header:
                f.write('%s\n' % output_line)
            
            for output_line in SPACECRAFT_KERNELS_TO_LOAD:
                f.write('%s\n' % output_line)
                
            for output_line in metakernel_footer:
                f.write('%s\n' % output_line)
    
    #return(sc_rec_tel_short)

def make_SPICEDirectories(spacecraft, basedir=''):
    
    #  Shape the spacecraft string and create a Path from the basedir
    spacecraft = spacecraft.lower().strip().replace(' ','')
    basedir = Path(basedir)
    SPICEdir = basedir / 'SPICE'
    
    #  Store the paths in a dictionary to be returned
    path_dict = {'spacecraft_kernel_dir': '',
                 'generic_kernel_dir'   : ''}
    
    path_dict['spacecraft_kernel_dir'] = SPICEdir / spacecraft / 'kernels/'

    path_dict['generic_kernel_dir'] = SPICEdir / 'generic' / 'kernels/'
    
    mk_name = 'metakernel_' + spacecraft + '.txt'
    metakernel_filepath = SPICEdir / spacecraft / mk_name
    
    #  Check that the directories exist
    for key, path in path_dict.items():
        if not os.path.exists(path):
            os.makedirs(path)
    
    return(path_dict, metakernel_filepath)

def get_MissionKernels(spacecraft, update_files=True):
    """A multi-line
    docstring.
    """
    
    baseurl = 'https://naif.jpl.nasa.gov/pub/naif/'
    
    path_info = pd.DataFrame(columns=['spk'], 
                             index=['url', 'savedir', 'filename_pattern'])
    match spacecraft:
        case 'juno':
            url = baseurl + 'pds/data/jno-j_e_ss-spice-6-v1.0/jnosp_1000/data/spk/'
            filename_pattern = '*juno_rec_??????_??????_??????*'
            #filetype = ['.bsp', '.lbl']
            return(None)
        
        case 'pioneer10':
            path_info['spk']['url'] = baseurl + 'PIONEER10/kernels/spk/'
            path_info['spk']['filename_pattern'] = '*.bsp'
            
        case 'pioneer11':
            path_info['spk']['url'] = baseurl + 'PIONEER11/kernels/spk/'
            path_info['spk']['filename_pattern'] = '*.bsp'
            
        case _:
            return(None)
    
    path_info['spk']['savedir'] = spacecraft_k_dir / 'spk/'
    
    
    for column in path_info:
        if (not pd.isna(column['url']) and 
            not pd.isna(column['savedir']) and 
            not pd.isna(column['namepattern']):
                
            run_wgetForSPICE(column['url'], 
                             column['savedir'], 
                             column['namepattern'])
    return()

def get_GenericKernels(generic_kernel_dir):
    """
    The generic kernels retrieved by this program are sufficient for playing
    around with SPICE, but are by no means exhaustive of those one would need
    for research purposes.
    
    Maybe one day this will be broader in scope, but for now there are too many
    trade-offs (filesize vs duration, loading of necessary vs unnecessary 
    planetary ephemerides, etc.) to consider.
    """
    import platform
    
    #  Check OS, which changes some file suffixes
    current_os = platform.system()
    
    if type(generic_kernel_dir) == str:
        generic_kernel_dir = Path(generic_kernel_dir)
    
    #  Base SPICE kernel URL
    baseurl = 'https://naif.jpl.nasa.gov/pub/naif/'
    
    path_info = pd.DataFrame(columns=['dsk', 'fk', 'lsk', 'pck', 'spk', ], 
                             index=['url', 'savedir', 'namepattern'])
    
    #  DSK INFO
    #  FK INFO
    #  LSK INFO
    suffix = '.tls'
    if 'Windows' in current_os: suffix += '.pc'
    path_info['lsk']['url']         = 'generic_kernels/lsk/'
    path_info['lsk']['savedir']     = generic_kernel_dir / 'lsk/'
    path_info['lsk']['namepattern'] = ['naif????',
                                        'latest_leapseconds']
    
    #  PCK INFO
    #  SPK INFO
    suffix = '.bsp'
    path_info['spk']['url']         = 'generic_kernels/spk/planets/'
    path_info['spk']['savedir']     = generic_kernel_dir / 'spk/planets/'
    path_info['spk']['namepattern'] = ['de440s']
    
    #  Loop over each column, getting the file
    for column in path_info:
        if (not pd.isna(column['url']) and 
            not pd.isna(column['savedir']) and 
            not pd.isna(column['namepattern']):
                
            run_wgetForSPICE(column['url'], 
                             column['savedir'], 
                             column['namepattern'])
        
    #  Return filepaths of downloaded files
    
    return()

def run_wgetForSPICE(url, savedir, namepattern):
    
    #  In case savedir is being handled as a pathlib Path, which subprocess
    #  doesn't like
    savedir = str(savedir)
    
    commandname = ['wget']
    
    #  A bunch of flags with this command call:
    #  -r: recursive
    #  -R *.html: reject .html files
    #  -np: don't ascend to the parent directory and go looking for files
    #  --directory-prefix: where to copy the files to
    #  -nH: no host directory (i.e. 'https://...')
    #  -nd: copy all files to this directory (could be --cut-dirs=#...)
    #  -s-show_progress: give a loading bar showing download time
    #  -q: quiet, don't show any other info
    flags = ['-r', '-R', '*.html', '-np', 
              '--directory-prefix=' + savedir, 
              '-nH', '-nd', '--show-progress', '-q']
    
    filepattern_flags = ['--accept=' + namepattern]
    host_url = [url]

    commandline = commandname + flags + filepattern_flags + host_url

    subprocess.run(commandline)

def make_Metakernel(spacecraft, basedir = '', update_files = True):
    
    #  Get paths to store SPICE kernels, including the metakernel
    path_dict, mk_filepath = make_SPICEDirectories(spacecraft, basedir)
    
    
    
    
    
    
    

    
    
    #  Now that you downloaded all the received Juno telemetry from the front-facing NAIF database
    #  Read the file names and construct a metakernel
    

    metakernel_header = ["# The meta kernel file contains entries pointing to the following SPICE kernels, which the user needs to download.",
                          "#",
                          "#   The following is the contents of a metakernel that was saved with",
                          "#   the name '" + mk_name + ".'",
                          "\\begindata",
                          "    PATH_VALUES = (",
                          "        '" + str(spacecraft_k_dir) + "'",
                          "        '" + str(generic_k_dir) + "'",
                          "        )",
                          "    PATH_SYMBOLS = (",
                          "        'SPACECRAFT',",
                          "        'GENERIC'",
                          "        )",
                          "    KERNELS_TO_LOAD = (",
                          "        '$GENERIC/lsk/latest_leapseconds.tls'"]
    metakernel_footer = ["        )",
                          "\\begintext"]


    # =============================================================================
    # Format spacecraft telemetry files for printing
    # =============================================================================
    spacecraft_kernels_to_load = []
    
    for column in path_info:
        
        filepaths = list(path_info[column]['savedir'].glob(path_info[column]['filename_pattern']))
        
        filenames = [filepath.name for filepath in filepaths]
        filenames.sort()
        
        filepaths_for_mk = [Path('$SPACECRAFT') / column / filename for filename in filenames]
        
        formatted_strings = ["\t'" + str(filepath) + "'" for filepath in filepaths_for_mk] 
        
        spacecraft_kernels_to_load.extend(formatted_strings)
    
    
    check = 'n'
    if os.path.exists(mk_filepath):
        print('Metakernel text file: ' + str(mk_filepath) + ' already exists.')
        check = input('Would you like to overwrite it? (y/n)  ')
    else:
        check = 'y'
    
    if check == 'y':
        with open(mk_filepath, mode='w') as f:
            for output_line in metakernel_header:
                f.write('%s\n' % output_line)
            
            for output_line in spacecraft_kernels_to_load:
                f.write('%s\n' % output_line)
                
            for output_line in metakernel_footer:
                f.write('%s\n' % output_line)
    
    #return(sc_rec_tel_short)
    
    return()