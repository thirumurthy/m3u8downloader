# -*- coding:utf-8 -*-
import sys
import os
import pbs
import requests
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import shutil
import time
import threading

cwd = os.getcwd()


def download_ts(path, url_list):
	ts_files = []
	for url in url_list:
		ts_name = url.split("/")[-1:]
		ts_file = os.path.join(path, ts_name[0])
		if os.path.exists(ts_file):
			ts_files.append(ts_file)
			continue
		with open(ts_file, 'wb') as f:
			tsmpath= "http://xlbor33arvaj-hls-live.wmncdn.net/peppers/live.stream/tracks-v1a1/"
			alblStatus.configure(text='Status: Downloading ts file ' + tsmpath + url)
			alblStatus.update()
			data = requests.get(tsmpath+url, stream=True)
			for chunk in data.iter_content(chunk_size=512):
				if chunk:
					f.write(chunk)
			alblStatus.configure(text='Status: sleeping 5 sec')
			alblStatus.update()
			time.sleep(5)  # Delays for 5 seconds. You can also use a float value.
		ts_files.append(ts_file)
	return ts_files


def startDownload():
	daction.configure(text='Downloading.. ')
	daction.update()
	alblStatus.configure(text='Status: Downloading.. ')
	alblStatus.update()
	ts_list = []
	mp4_file = None
	m3u8link = "http://xlbor33arvaj-hls-live.wmncdn.net/peppers/live.stream/index.m3u8"
	m3u8path = "http://xlbor33arvaj-hls-live.wmncdn.net/peppers/live.stream/"
	alblStatus.configure(text='Status: Downloading.. '+ m3u8link)
	alblStatus.update()
	m3u8_file = requests.get(m3u8link).text
	mp4_file = "test.mp4"
	print(m3u8_file, mp4_file)
	for line in m3u8_file.splitlines():
		if line.endswith(".ts\n") or line.endswith(".ts"):
			ts_list.append(line.replace("\n", ""))
		if (line.endswith(".m3u8")):
			alblStatus.configure(text='Status: Downloading.. ' + m3u8path + line)
			alblStatus.update()
			nm3u8_file = requests.get( m3u8path + line).text
			for nline in nm3u8_file.splitlines():
				if nline.endswith(".ts\n") or nline.endswith(".ts"):
					ts_list.append(nline.replace("\n", ""))
	ts_path = os.path.join(cwd, "ts_files")
	if not os.path.exists(ts_path):
		os.makedirs(ts_path)

	ts_file_list = download_ts(ts_path, ts_list)

	print(ts_file_list)
	alblStatus.configure(text='Status: Download Finished ..  Merging process started.')
	alblStatus.update()
	mp4_path = os.path.join(cwd, mp4_file)

	with open(mp4_path, 'ab') as f:
		for ts_file in ts_file_list:
			with open(ts_file, "rb") as ts:
				f.write(ts.read())
	alblStatus.configure(text='Status: Cleaning temp folder..')
	alblStatus.update()
	shutil.rmtree(ts_path)
	alblStatus.configure(text='Status: file saved to ' + mp4_path)
	alblStatus.update()
	daction.configure(text='Start Download')
	daction.update()

# button click event
def clickMe():
	action.configure(text='Hello ' + name.get())
if __name__=='__main__':
	argv_len = len(sys.argv)
	# window
	win = tk.Tk()
	win.title("M3U8 Video Downloader.")
	# win.resizable(0,0)
	win.geometry("500x300")

	# modify adding label
	aLabel = ttk.Label(win, text="A Label")
	aLabel.grid(column=0, row=0)


	# text box entry
	ttk.Label(win, text="Enter a name:").grid(column=0, row=0)
	name = tk.StringVar()
	nameEntered = ttk.Entry(win, width=12, textvariable=name)
	nameEntered.grid(column=0, row=1)

	# button
	action = ttk.Button(win, text="Click Me!", command=clickMe)
	action.grid(column=2, row=1)
	# action.configure(state='disabled')

	# drop down menu
	ttk.Label(win, text="Choose a TV Channel:").grid(column=1, row=0)
	tvchannel = tk.StringVar()
	tvChosen = ttk.Combobox(win, width=12, textvariable=tvchannel)
	tvChosen['values'] = ('Peppers TV', 'Tune 6')
	tvChosen.grid(column=1, row=1)
	tvChosen.current(1)

	alblStatus = ttk.Label(win, text="Status: None")
	alblStatus.grid(column=0, row=3)

	def beginDownload():
		threading.Thread(target=startDownload()).start()

	# button
	daction = ttk.Button(win, text="Start Download", command=beginDownload)
	daction.grid(column=0, row=2)
	win.mainloop()
	# Best example GIT
	# copied from https://gist.github.com/nick3499/be70339ccb12f735a55a23ca7869e492