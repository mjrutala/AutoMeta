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

def get_SpacecraftKernels(spacecraft, spacecraft_kernel_dir):
    """
    
    """
    #  Shape the spacecraft string 
    spacecraft = spacecraft.lower().strip().replace(' ','')
    
    baseurl = 'https://naif.jpl.nasa.gov/pub/naif/'
    
    path_info = pd.DataFrame(columns=['fk', 'spk'], 
                             index=['url', 'savedir', 'namepattern'])
    match spacecraft:

        case 'pioneer10':
            path_info['spk']['url'] = [baseurl + 'PIONEER10/kernels/spk/']
            path_info['spk']['namepattern'] = ['*.bsp']
            
        case 'pioneer11':
            path_info['spk']['url'] = [baseurl + 'PIONEER11/kernels/spk/']
            path_info['spk']['namepattern'] = ['*.bsp']
            
        case 'voyager1':
            path_info['spk']['url'] = [baseurl + 'VOYAGER/kernels/spk/']
            path_info['spk']['namepattern'] = ['Voyager_1.a54206u_V0.2_merged.bsp']
            
        case 'voyager2':
            path_info['spk']['url'] = [baseurl + 'VOYAGER/kernels/spk/']
            path_info['spk']['namepattern'] = ['Voyager_2.m05016u.merged.bsp']
            
        case 'cassini':
            path_info['spk']['url'] = [baseurl + 'CASSINI/kernels/spk/']
            path_info['spk']['namepattern'] = ['200128RU_SCPSE_?????_?????.bsp']
            
            
        case 'juno':
            path_info['spk']['url'] = [baseurl + 'pds/data/jno-j_e_ss-spice-6-v1.0/jnosp_1000/data/spk/']
            path_info['spk']['namepattern'] = ['*juno_rec_??????_??????_??????*.bsp']
            
            path_info['fk']['url'] = [baseurl + 'pds/data/jno-j_e_ss-spice-6-v1.0/jnosp_1000/data/fk/']
            path_info['fk']['namepattern'] = ['juno_v??.*']
        case _:
            return(None)
    
    path_info['fk']['savedir'] = [spacecraft_kernel_dir / 'fk']
    path_info['spk']['savedir'] = [spacecraft_kernel_dir / 'spk']
    
    
    #  Loop over each column, getting the file
    #  This is a horrible, horrible loop
    retrieved_files = list()
    for columnname, column in path_info.items():
        if not pd.isna(column).any():
            for url in column['url']:
                for savedir in column['savedir']:
                    for namepattern in column['namepattern']:
                        #  Get the file with wget
                        run_wgetForSPICE(url, savedir, namepattern)
                        
                        #  Look for the files
                        retrieved_files.extend(list(savedir.glob(namepattern)))
    return(retrieved_files)

def get_GenericKernels(generic_kernel_dir, basedir=''):
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
                             index=['url', 'namepattern'])
    
    #  DSK INFO
    #  FK INFO
    #  LSK INFO
    suffix = '.tls'
    if 'Windows' in current_os: suffix += '.pc'
    path_info['lsk']['url']         = [baseurl + 'generic_kernels/lsk/']
    #path_info['lsk']['savedir']     = [generic_kernel_dir / 'lsk']
    path_info['lsk']['namepattern'] = ['naif????' + suffix,
                                       'latest_leapseconds' + suffix]
    
    #  PCK INFO
    suffix = '.tpc'
    path_info['pck']['url']         = [baseurl + 'generic_kernels/pck/']
    #path_info['pck']['savedir']     = [generic_kernel_dir / 'pck']
    path_info['pck']['namepattern'] = ['pck00011' + suffix]
    
    #  SPK INFO
    suffix = '.bsp'
    path_info['spk']['url']         = [baseurl + 'generic_kernels/spk/planets/',
                                       baseurl + 'generic_kernels/spk/satellites/']
    #path_info['spk']['savedir']     = [generic_kernel_dir / 'spk' / 'planets',
    #                                   generic_kernel_dir / 'spk' / 'satellites']
    path_info['spk']['namepattern'] = ['de440s' + suffix,
                                       'jup365' + suffix,
                                       'sat441' + suffix]
    
    #  Loop over each column, getting the file
    #  This is a horrible, horrible loop
    retrieved_files = list()
    for columnname, column in path_info.items():
        if not pd.isna(column).any():
            for url in column['url']:
                for namepattern in column['namepattern']:
                    #
                    savedir_parts = Path(url.replace(baseurl, '')).parts[1:]
                    savedir = generic_kernel_dir
                    for part in savedir_parts: savedir = savedir / part
                    print(savedir)
                    
                    #  Get the file with wget
                    run_wgetForSPICE(url, savedir, namepattern)
                    
                    #  Look for the files
                    retrieved_files.extend(list(savedir.glob(namepattern)))
    #  Return filepaths of downloaded files
    
    return(retrieved_files)

def run_wgetForSPICE(url, savedir, namepattern, show_progress=True):
    
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
    flags = ['-r', '-R', '*.html', '-np', '--level=1',
             '--directory-prefix=' + savedir, 
             '-nH', '-nd', '-q']
    if show_progress:
        flags.append('--show-progress')
    
    filepattern_flags = ['--accept=' + namepattern]
    host_url = [url]

    commandline = commandname + flags + filepattern_flags + host_url
    
    subprocess.run(commandline)

def make_Metakernel(spacecraft, basedir = ''):
    
    #  Get paths to store SPICE kernels, including the metakernel
    path_dict, mk_filepath = make_SPICEDirectories(spacecraft, basedir)
    
    generic_kernel_filepaths = get_GenericKernels(path_dict['generic_kernel_dir'])
    
    spacecraft_kernel_filepaths = get_SpacecraftKernels(spacecraft, path_dict['spacecraft_kernel_dir'])

    #  Now that you downloaded all the received Juno telemetry from the front-facing NAIF database
    #  Read the file names and construct a metakernel
    
    metakernel_header =  ["# The meta kernel file contains entries pointing to the following SPICE kernels, which the user needs to download.",
                          "#",
                          "#   The following is the contents of a metakernel that was saved with",
                          "#   the name '" + mk_filepath.name + ".'",
                          "\\begindata",
                          "    PATH_VALUES = (",
                          "        '" + str(path_dict['generic_kernel_dir']) + "'",
                          "        '" + str(path_dict['spacecraft_kernel_dir']) + "'",
                          "        )",
                          "    PATH_SYMBOLS = (",
                          "        'GENERIC'",
                          "        'SPACECRAFT',",
                          "        )",
                          "    KERNELS_TO_LOAD = ("]
    metakernel_footer =  ["        )",
                          "\\begintext"]

    #return(generic_kernel_filepaths, spacecraft_kernel_filepaths)
    # =============================================================================
    # Format spacecraft telemetry files for printing
    # =============================================================================
    generic_path_str_to_write = list()
    spacecraft_path_str_to_write = list()
    
    
    for filepath in generic_kernel_filepaths:
        rel_filepath = Path(os.path.relpath(filepath, path_dict['generic_kernel_dir']))
        
        #   We don't need to write leap second files, since the 
        #  'latest_leapseconds' file points to them
        if 'lsk' + os.sep + 'naif' not in str(rel_filepath):
            formatted_path = Path('$GENERIC') / rel_filepath
            formatted_path_str = "\t'" + str(formatted_path) + "'"
            generic_path_str_to_write.append(formatted_path_str)
    generic_path_str_to_write.sort()
            
    for filepath in spacecraft_kernel_filepaths:
        rel_filepath = Path(os.path.relpath(filepath, path_dict['spacecraft_kernel_dir']))
        
        #  The Metakernel doesn't care about label files, those are for you
        if '.lbl' not in str(rel_filepath):
            formatted_path = Path('$SPACECRAFT') / rel_filepath
            formatted_path_str = "\t'" + str(formatted_path) + "'"
            spacecraft_path_str_to_write.append(formatted_path_str)
    spacecraft_path_str_to_write.sort()
    
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
            
            for output_line in generic_path_str_to_write:
                f.write('%s\n' % output_line)   
            
            for output_line in spacecraft_path_str_to_write:
                f.write('%s\n' % output_line)
                
            for output_line in metakernel_footer:
                f.write('%s\n' % output_line)
    
    return(mk_filepath)

# def deprecated_generate_JunoMetakernel(update_files = False):
#     import subprocess
#     import os
#     import glob
    
#     output_file = '/Users/mrutala/SPICE/juno/metakernel_juno.txt'
    
#     filepattern = '*juno_rec_??????_??????_??????*'
#     #filetype = ['.bsp', '.lbl']
    
#     destination_dir = '/Users/mrutala/SPICE/juno/kernels/spk/'
    
#     command = ['wget']
#     flags = ['-r', '-R', '*.html', '-np', '--directory-prefix=' + destination_dir, '-nv', '-nH', '--cut-dirs=8', '--show-progress', '-q']
#     filepattern_flags = ['--accept=' + filepattern]
#     host_url = ['https://naif.jpl.nasa.gov/pub/naif/pds/data/jno-j_e_ss-spice-6-v1.0/jnosp_1000/data/spk/']
    
#     line = command + flags + filepattern_flags + host_url
#     if update_files:
#         subprocess.run(line)
    
#     #  Now that you downloaded all the received Juno telemetry from the front-facing NAIF database
#     #  Read the file names and construct a metakernel
    

#     metakernel_header = ["# The meta kernel file contains entries pointing to the following SPICE kernels, which the user needs to download.",
#                          "#",
#                          "#   The following is the contents of a metakernel that was saved with",
#                          "#   the name 'metakernel_juno.txt'.",
#                          "\\begindata",
#                          "    PATH_VALUES = (",
#                          "        '/Users/mrutala/SPICE/juno/kernels/',",
#                          "        '/Users/mrutala/SPICE/generic/kernels/'",
#                          "        )",
#                          "    PATH_SYMBOLS = (",
#                          "        'SPACECRAFT',",
#                          "        'GENERIC'",
#                          "        )",
#                          "    KERNELS_TO_LOAD = (",
#                          "        '$GENERIC/lsk/latest_leapseconds.tls'"]
#     metakernel_footer = ["        )",
#                          "\\begintext"]


#     # =============================================================================
#     # Format spacecraft telemetry files for printing
#     # =============================================================================
#     SPACECRAFT_KERNELS_TO_LOAD = []
    
#     sc_rec_tel_long = glob.glob(destination_dir + 'juno_rec_orbit' + '.bsp')
#     sc_rec_tel_long_filenames = [os.path.basename(f) for f in sc_rec_tel_long]
#     sc_rec_tel_long_filenames.sort()
#     sc_rec_tel_long_filenames_formatted = ['\t' + "'$SPACECRAFT" + os.sep + 'spk' + os.sep + filename + "'" for filename in sc_rec_tel_long_filenames]
    
#     SPACECRAFT_KERNELS_TO_LOAD.extend(sc_rec_tel_long_filenames_formatted)
    
#     sc_rec_tel_short = glob.glob(destination_dir + filepattern[:-1] + '.bsp')
#     sc_rec_tel_short_filenames = [os.path.basename(f) for f in sc_rec_tel_short]
#     sc_rec_tel_short_filenames.sort()
#     sc_rec_tel_short_filenames_formatted = ['\t' + "'$SPACECRAFT" + os.sep + 'spk' + os.sep + filename + "'" for filename in sc_rec_tel_short_filenames]
    
#     SPACECRAFT_KERNELS_TO_LOAD.extend(sc_rec_tel_short_filenames_formatted)
    
#     check = 'n'
#     if os.path.exists(output_file):
#         print('Metakernel text file: ' + output_file + 'already exists.')
#         check = input('Would you like to overwrite it? (y/n)  ')
#     else:
#         check = 'y'
    
#     if check == 'y':
#         with open(output_file, mode='w') as f:
#             for output_line in metakernel_header:
#                 f.write('%s\n' % output_line)
            
#             for output_line in SPACECRAFT_KERNELS_TO_LOAD:
#                 f.write('%s\n' % output_line)
                
#             for output_line in metakernel_footer:
#                 f.write('%s\n' % output_line)
    
#     #return(sc_rec_tel_short)