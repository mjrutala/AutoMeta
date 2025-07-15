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
    if basedir == '':
        basedir = os.getcwd()
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

def get_SpacecraftKernels(spacecraft, spacecraft_kernel_dir, force_update=False, wget=False):
    """
    
    """
    #  Shape the spacecraft string 
    spacecraft = spacecraft.lower().strip().replace(' ','')
    
    baseurl = 'https://naif.jpl.nasa.gov/pub/naif/'
    
    path_info = pd.DataFrame(columns=['fk', 'spk'], 
                             index=['url', 'savedir', 'namepattern'])
    match spacecraft:

        case 'pioneer10':
            path_info.loc['url', 'spk'] = [baseurl + 'PIONEER10/kernels/spk/']
            path_info.loc['namepattern', 'spk'] = ['*.bsp']
            
        case 'pioneer11':
            path_info.loc['url', 'spk'] = [baseurl + 'PIONEER11/kernels/spk/']
            path_info.loc['namepattern', 'spk'] = ['*.bsp']
            
        case 'voyager1':
            path_info.loc['url', 'spk'] = [baseurl + 'VOYAGER/kernels/spk/']
            path_info.loc['namepattern', 'spk'] = ['Voyager_1.a54206u_V0.2_merged.bsp']
            
        case 'voyager2':
            path_info.loc['url', 'spk'] = [baseurl + 'VOYAGER/kernels/spk/']
            path_info.loc['namepattern', 'spk'] = ['Voyager_2.m05016u.merged.bsp']
            
        case 'cassini':
            path_info.loc['url', 'spk'] = [baseurl + 'CASSINI/kernels/spk/']
            path_info.loc['namepattern', 'spk'] = ['??????R_SCPSE_?????_?????.bsp', '??????RU_SCPSE_?????_?????.bsp']
            
            path_info.loc['url', 'fk'] = [baseurl + 'CASSINI/kernels/fk/']
            path_info.loc['namepattern', 'fk'] = ['cas_dyn_v??.*']
            
            
        case 'juno':
            #path_info['spk']['url'] = [baseurl + 'pds/data/jno-j_e_ss-spice-6-v1.0/jnosp_1000/data/spk/']
            path_info.loc['url', 'spk'] = [baseurl + 'JUNO/kernels/spk/']
            #path_info['spk']['namepattern'] = ['*juno_rec_??????_??????_??????*.bsp']
            path_info.loc['namepattern', 'spk'] = ['spk_rec_??????_??????_??????.bsp*']
            
            #path_info['fk']['url'] = [baseurl + 'pds/data/jno-j_e_ss-spice-6-v1.0/jnosp_1000/data/fk/']
            path_info.loc['url', 'fk'] = [baseurl + 'JUNO/kernels/fk/']
            path_info.loc['namepattern', 'fk'] = ['juno_v??.*']
            
        case 'messenger':
            path_info.loc['url', 'spk'] = [baseurl + 'pds/data/mess-e_v_h-spice-6-v1.0/messsp_1000/data/spk/']
            path_info.loc['namepattern', 'spk'] = ['msgr_??????_??????_recon_gsfc_1.bsp']  #  Excludes cruise phase
            
        case _:
            return(None)
    
    path_info.loc['savedir', 'fk'] = [spacecraft_kernel_dir / 'fk']
    path_info.loc['savedir', 'spk'] = [spacecraft_kernel_dir / 'spk']
    
    #  Loop over each column, getting the file
    #  This is a horrible, horrible loop
    retrieved_files = list()
    for columnname, column in path_info.items():
        if not pd.isna(column).any():
            for url in column['url']:
                for savedir in column['savedir']:
                    for namepattern in column['namepattern']:
                        
                        if wget:
                            #  Get the file with wget
                            run_wgetForSPICE(url, savedir, namepattern, force_update=force_update)
                        else:
                            # Try urrlib
                            run_urllibForSPICE(url, savedir, namepattern, force_update=force_update)
                    
                        #  Look for the files
                        retrieved_files.extend(list(savedir.glob(namepattern)))
    return(retrieved_files)

def get_GenericKernels(generic_kernel_dir, basedir='', force_update=False, wget=False):
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
    path_info.loc['url', 'lsk']         = [baseurl + 'generic_kernels/lsk/']
    #path_info['lsk']['savedir']     = [generic_kernel_dir / 'lsk']
    path_info.loc['namepattern', 'lsk'] = ['naif????' + suffix,
                                       'latest_leapseconds' + suffix]
    
    #  PCK INFO
    suffix = '.tpc'
    path_info.loc['url', 'pck']        = [baseurl + 'generic_kernels/pck/']
    #path_info['pck']['savedir']     = [generic_kernel_dir / 'pck']
    path_info.loc['namepattern', 'pck'] = ['pck00011' + suffix]
    
    #  SPK INFO
    suffix = '.bsp'
    path_info.loc['url', 'spk']         = [baseurl + 'generic_kernels/spk/planets/',
                                       baseurl + 'generic_kernels/spk/satellites/']
    #path_info['spk']['savedir']     = [generic_kernel_dir / 'spk' / 'planets',
    #                                   generic_kernel_dir / 'spk' / 'satellites']
    path_info.loc['namepattern', 'spk'] = ['de440s' + suffix,
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
                    # print(savedir)
                    
                    if wget:
                        #  Get the file with wget
                        run_wgetForSPICE(url, savedir, namepattern, force_update=force_update)
                    else:
                        # Try urrlib
                        run_urllibForSPICE(url, savedir, namepattern, force_update=force_update)
                    
                    #  Look for the files
                    retrieved_files.extend(list(savedir.glob(namepattern)))
    #  Return filepaths of downloaded files
    
    return(retrieved_files)

def run_wgetForSPICE(url, savedir, namepattern, show_progress=True, force_update=False):
    
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
    #  --timestamping: use time-stamping, which should only download missing or updated files
    flags = ['-r', '-np', '--level=1',
             '--directory-prefix=' + savedir, 
             '-nH', '-nd', '-q']
    if not force_update:
        flags.append('--timestamping')
    if show_progress:
        flags.append('--show-progress')
    
    filepattern_flags = ['--accept=' + namepattern, '--reject=*.html']
    host_url = [url]

    commandline = commandname + flags + filepattern_flags + host_url
    
    subprocess.run(commandline, check=True)

def run_urllibForSPICE(url, savedir, namepattern, show_progress=True, force_update=False):
    import urllib.request
    import re
    from fnmatch import fnmatch
    import tqdm
    
    # #  In case savedir is being handled as a pathlib Path, which subprocess
    # #  doesn't like
    # savedir = str(savedir)
    
    # html_url = url
    with urllib.request.urlopen(url) as response:
        html_body = response.read().decode('utf-8')
    
    # Three-part filtering, for interpretability
    # First, filter the html for all hrefs (links)
    href_pattern = r'href=["\']([^"\']*)["\']'
    href_list = re.findall(href_pattern, html_body)
    
    # Second, remove weblinks (we only want files
    file_list = [l for l in href_list if not l.startswith('http')]

    # Third, match the remaining files to our namepattern
    matching_file_list = [l for l in file_list if fnmatch(l, namepattern)]
        
    # Now download
    for f in tqdm.tqdm(matching_file_list, desc='Downloading to {}'.format(savedir)):
        if not savedir.is_dir():
            savedir.mkdir(parents=True)
        filepath = savedir / f
        urllib.request.urlretrieve(url, filepath)
    
    return
    
def make_Metakernel(spacecraft, basedir = '', force_update=False):
    
    #  Get paths to store SPICE kernels, including the metakernel
    path_dict, mk_filepath = make_SPICEDirectories(spacecraft, basedir)
    
    generic_kernel_filepaths = get_GenericKernels(path_dict['generic_kernel_dir'], force_update=force_update)   
    
    spacecraft_kernel_filepaths = get_SpacecraftKernels(spacecraft, path_dict['spacecraft_kernel_dir'], force_update=force_update)
    
    #  Now that you downloaded all the received Juno telemetry from the front-facing NAIF database
    #  Read the file names and construct a metakernel
    
    metakernel_header =  ["# The meta kernel file contains entries pointing to the following SPICE kernels, which the user needs to download.",
                          "#",
                          "#   The following is the contents of a metakernel that was saved with",
                          "#   the name '" + mk_filepath.name + ".'",
                          "\\begindata",
                          "    PATH_VALUES = (",
                          "        '" + str(basedir / path_dict['generic_kernel_dir']) + "'",
                          "        '" + str(basedir / path_dict['spacecraft_kernel_dir']) + "'",
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

if __name__ == "__main__":
    spacecraft = input('Name of target spacecraft:')
    basedir = input('Path to directory containing the SPICE base directory (press enter for current directory):')
    result = make_Metakernel(spacecraft, basedir = basedir)
    print('Finished!')
    print('SPICE MetaKernel for {} wrtten to: {}'.format(spacecraft, result))
