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

def audio_hook(d):
    #final_filename  = d.get('info_dict').get('filepath')
    #print(f'final_filename : {final_filename}')
    window['-TOUT1-'].update(d['status'])
    #window['-TOUT1-'].update(final_filename)
    window.refresh()

def video_hook(d):
    window['-TOUT2-'].update(d['status'])
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
        'progress_hooks': [audio_hook],
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
    return rtnval

def download_video(url, dlfn, folder) :
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
        'format': 'best[ext=mp4]',
        'outtmpl': dlfilename,
        'progress_hooks': [video_hook],
    }
    try :
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            #info = ydl.extract_info(url, download=True)
            ydl.download(urls)
            rtnval = "Video Downloaded"
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
    return rtnval


# --------------------------------- Define Layout ---------------------------------

# First the window layout...2 columns
final_filename  = ""

one_col = [
    [sg.Text('Url'), sg.In(size=(40,2), enable_events=True ,key='-URL-')],    
    [sg.Text('Download filename'), sg.In(size=(40,2), enable_events=True ,key='-DLFN-')],    
    [sg.Text('Download Folder'), sg.In(size=(40,2), enable_events=True ,key='-FOLDER-'), sg.FolderBrowse()],
    [sg.Checkbox('Video', enable_events=True, key='-VIDEOCB-', disabled = False), sg.Checkbox('Audio', enable_events=True, key='-AUDIOCB-', disabled = False)],
    [sg.Text(size=(40,2), key='-TOUT1-')],
    [sg.Text(size=(40,2), key='-TOUT2-')],
    [sg.Button(button_text = "Download", disabled = True,key='-Download-'), sg.Exit()]
]

# ----- Full layout -----
layout = [[sg.Column(one_col, element_justification='c')]]

# --------------------------------- Create Window ---------------------------------
window = sg.Window('Audio Downloader', layout,resizable=True)

# ----- Run the Event Loop -----
# --------------------------------- Event Loop ---------------------------------
folder = ""
url = ""
dlfn = ""

audiocb = False
videocb = False

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == '-FOLDER-':  # Download Folder name entered
        folder = values['-FOLDER-']
        window['-TOUT1-'].update("")
        window['-TOUT2-'].update("")
        if folder != "" and url != "" and dlfn != "" and (audiocb or videocb):
            window['-Download-'].update(disabled = False)
        else :
            window['-Download-'].update(disabled = True)
    elif event == '-URL-':    # url entered
        url = values['-URL-'] 
        window['-TOUT1-'].update("")
        window['-TOUT2-'].update("")
        if folder != "" and url != "" and dlfn != "" and (audiocb or videocb):
            window['-Download-'].update(disabled = False)
        else :
            window['-Download-'].update(disabled = True)
    elif event == '-DLFN-':    # Download Filename entered
        dlfn = values['-DLFN-'] 
        window['-TOUT1-'].update("")
        window['-TOUT2-'].update("")
        if folder != "" and url != "" and dlfn != "" and (audiocb or videocb):
            window['-Download-'].update(disabled = False)
        else :
            window['-Download-'].update(disabled = True)
    elif event == '-AUDIOCB-':    # Audio Checkbox
        window['-TOUT1-'].update("")
        window['-TOUT2-'].update("")
        audiocb = values['-AUDIOCB-'] 
        if folder != "" and url != "" and dlfn != "" and (audiocb or videocb):
            window['-Download-'].update(disabled = False)
        else :
            window['-Download-'].update(disabled = True)
    elif event == '-VIDEOCB-':    # Audio Checkbox
        window['-TOUT1-'].update("")
        window['-TOUT2-'].update("")
        videocb = values['-VIDEOCB-']  
        if folder != "" and url != "" and dlfn != "" and (audiocb or videocb):
            window['-Download-'].update(disabled = False)
        else :
            window['-Download-'].update(disabled = True)
    elif event == '-Download-': 
        try:
            window['-Download-'].update(disabled = True)
            if videocb :
                rtnval = download_video(url,dlfn, folder)
                window['-TOUT2-'].update(rtnval)
            if audiocb :
                rtnval = download_audio(url,dlfn, folder)
                window['-TOUT1-'].update(rtnval)
            window['-URL-'].update('')
            window['-DLFN-'].update('')
            window['-VIDEOCB-'].update(value =  False)
            window['-AUDIOCB-'].update(value =  False)
            url = ""
            dlfn = ""
            audiocb = False
            videocb = False
            window['-URL-'].set_focus(force = True)
            window.refresh()
        except Exception as E:
            #print(f'** Error {E} **')
            pass        # something weird happened making the full filename

# --------------------------------- Close & Exit ---------------------------------
window.close()