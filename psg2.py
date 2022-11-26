import PySimpleGUI as sg
import os.path
import json
import yt_dlp 

"""
    Demo for displaying any format of image file.

    Normally tkinter only wants PNG and GIF files.  This program uses PIL to convert files
    such as jpg files into a PNG format so that tkinter can use it.

    The key to the program is the function "convert_to_bytes" which takes a filename or a 
    bytes object and converts (with optional resize) into a PNG formatted bytes object that
    can then be passed to an Image Element's update method.  This function can also optionally
    resize the image.

    Copyright 2020 PySimpleGUI.org
"""

def my_hook(d):
    #final_filename  = d.get('info_dict').get('filepath')
    #print(f'final_filename : {final_filename}')
    window['-TOUT-'].update(d['status'])
    #window['-TOUT-'].update(final_filename)
    window.refresh()

def download_audio(url, dlfn, folder) :
    '''
    Will download audio from url
    :param url: url to download audio from
    :type url:  string
    :param dlfn: Filename to save the downloaded audio
    :type dlfn:  string
    :param folder: Folder for the downloaded audio file
    :type folder:  string
    :return: string
    :rtype: string
    '''
    urls = []
    urls.append(url)
    dlfilename = folder + '/' + dlfn + '.%(ext)s'
    #filename = os.path.normpath(folder + '/' + dlfn + '.%(ext)s')
    print(dlfilename)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': dlfilename,
        'progress_hooks': [my_hook],
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
            }],
    }
    try :
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            #info = ydl.extract_info(url, download=True)
            ydl.download(urls)
            rtnval = "Audio Downloaded"
            #file_path = ydl.prepare_filename(info, outtmpl= dlfilename)

        #print(type(info))
        #print(file_path)
        #details = ydl.sanitize_info(info)
        #with open(os.path.normpath(folder + '/rkntest.txt'),'w') as data: 
        #    data.write(str(details))
        #print(type(details))
        # ℹ️ ydl.sanitize_info makes the info json-serializable
        #print(json.dumps(ydl.sanitize_info(info)))
        #with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        #    ydl.download(urls)
    except Exception as e:
        rtnval = f'** Error {e} **'
        print(type(rtnval))
    return rtnval

# --------------------------------- Define Layout ---------------------------------

# First the window layout...2 columns
final_filename  = ""

left_col = [
    [sg.Text('Url'), sg.In(size=(40,2), enable_events=True ,key='-URL-')],    
    [sg.Text('Download filename'), sg.In(size=(40,2), enable_events=True ,key='-DLFN-')],    
    [sg.Text('Download Folder'), sg.In(size=(40,2), enable_events=True ,key='-FOLDER-'), sg.FolderBrowse()],
[sg.Text(size=(40,2), key='-TOUT-')],
              [sg.Button(button_text = "Download", disabled = True,key='-Download-'), sg.Exit()]
]

# ----- Full layout -----
layout = [[sg.Column(left_col, element_justification='c')]]

# --------------------------------- Create Window ---------------------------------
window = sg.Window('Audio Downloader', layout,resizable=True)

# ----- Run the Event Loop -----
# --------------------------------- Event Loop ---------------------------------
folder = ""
url = ""
dlfn = ""

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == '-FOLDER-':  # Download Folder name entered
        folder = values['-FOLDER-']
        window['-TOUT-'].update("")
        if folder != "" and url != "" and dlfn != "":
            window['-Download-'].update(disabled = False)
    elif event == '-URL-':    # url entered
        url = values['-URL-'] 
        window['-TOUT-'].update("")
        if folder != "" and url != "" and dlfn != "":
            window['-Download-'].update(disabled = False)
    elif event == '-DLFN-':    # Download Filename entered
        dlfn = values['-DLFN-'] 
        window['-TOUT-'].update("")
        if folder != "" and url != "" and dlfn != "":
            window['-Download-'].update(disabled = False)
    elif event == '-Download-': 
        try:
            window['-Download-'].update(disabled = True)
            rtnval = download_audio(url,dlfn, folder)
            window['-TOUT-'].update(rtnval)
            window['-URL-'].update('')
            window['-DLFN-'].update('')
            url = ""
            dlfn = ""
            window['-URL-'].set_focus(force = True)
            window.refresh()
        except Exception as E:
            #print(f'** Error {E} **')
            pass        # something weird happened making the full filename

# --------------------------------- Close & Exit ---------------------------------
window.close()