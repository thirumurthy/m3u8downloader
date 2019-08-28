from flask import Flask  
  
app = Flask(__name__) #creating the Flask class object   
 
@app.route('/') #decorator drfines the   
def home():  
    return "hello, this is our first flask website";  
  




def download_ts(domain, path, url_list):
	ts_files = []
	for url in url_list:
		ts_name = url.split("/")[-1:]
		ts_file = os.path.join(path, ts_name[0])
		if os.path.exists(ts_file):
			ts_files.append(ts_file)
			continue
		with open(ts_file, 'wb') as f:
			data = requests.get(domain + url, stream=True)
			for chunk in data.iter_content(chunk_size=512):
				if chunk:
					f.write(chunk)
		ts_files.append(ts_file)
	return ts_files





if __name__ =='__main__':  
    app.run(debug = True)  
