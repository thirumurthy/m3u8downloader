# -*- coding:utf-8 -*-
import sys
import os
import pbs
import requests
import tkinter as tk 

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
			data = requests.get("http://xlbor33arvaj-hls-live.wmncdn.net/peppers/live.stream/tracks-v1a1/"+url, stream=True)
			for chunk in data.iter_content(chunk_size=512):
				if chunk:
					f.write(chunk)
		ts_files.append(ts_file)
	return ts_files




if __name__=='__main__':
	argv_len = len(sys.argv)

	ts_list = []
	mp4_file = None

	r = tk.Tk() 
	r.title('M3U8 Video Downloader.')
	r.geometry("500x300")
	statusTxt = "Status:"
	label = tk.Label(r, text=statusTxt)
	label.pack()
	button = tk.Button(r, text='Stop', width=25, command=r.destroy) 
	button.pack() 
	statusTxt = "Status: starting.."
	if 3 == 3:
		m3u8_file = requests.get("http://xlbor33arvaj-hls-live.wmncdn.net/peppers/live.stream/index.m3u8").text
		mp4_file = "test.mp4"
		print(m3u8_file, mp4_file)
		for line in m3u8_file.splitlines():
			if line.endswith(".ts\n") or line.endswith(".ts"):
				ts_list.append(line.replace("\n", ""))
			if(line.endswith(".m3u8")):
				nm3u8_file = requests.get("http://xlbor33arvaj-hls-live.wmncdn.net/peppers/live.stream/"+line).text
				for nline in nm3u8_file.splitlines():
					if nline.endswith(".ts\n") or nline.endswith(".ts"):
						ts_list.append(nline.replace("\n", ""))

	ts_path = os.path.join(cwd, "ts_files")
	if not os.path.exists(ts_path):
		os.makedirs(ts_path)

	ts_file_list = download_ts(ts_path, ts_list)


	print(ts_file_list)

	mp4_path = os.path.join(cwd, mp4_file)
	 
	with open(mp4_path, 'ab') as f:
		for ts_file in ts_file_list:
			with open(ts_file, "rb") as ts:
				f.write(ts.read())
	
	r.mainloop()
	os.remove(ts_path)