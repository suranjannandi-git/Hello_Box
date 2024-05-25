import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
ACCESS_TOKEN_IBM_BOX = os.getenv("ACCESS_TOKEN_IBM_BOX")

#upload the file to box
def upload_file_to_box(upload_file_path, folder_id):
    BOX_UPLOAD_FILE_API = "https://upload.box.com/api/2.0/files/content"
    headersAPI = {'Authorization': 'Bearer ' + ACCESS_TOKEN_IBM_BOX}

    files = {
        'attributes': (None, '{"name":"' + upload_file_path.split('/')[-1] + '", "parent":{"id":"' + folder_id + '"}}'),
        'file': (upload_file_path, open(upload_file_path, 'rb'))
    }
    response = requests.post(BOX_UPLOAD_FILE_API, headers=headersAPI, files=files)
    # close the file
    files['file'][1].close()

    if response.status_code == 201:
        response_content = json.loads(response.content)
        file_id = response_content['entries'][0]['id']
        file_url = 'https://app.box.com/file/' + file_id
        print("File uploaded successfully, ", file_url)
        return file_url
    else:
        print("Failed to upload file, please delete if file already exists in box")
        return None

# Download file from box folder
def download_file_from_box(box_file_id, target_file):
    BOX_DOWNLOAD_FILE_API = "https://api.box.com/2.0/files/" + str(box_file_id) + "/content"
    headersAPI = {'Authorization': 'Bearer ' + ACCESS_TOKEN_IBM_BOX}

    # Check if the directory exists, if not, create it
    directory = os.path.dirname(target_file)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with requests.get(BOX_DOWNLOAD_FILE_API, headers=headersAPI, stream=True) as r:
        r.raise_for_status()
        with open(target_file, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    print("File downloaded successfully ", target_file)
    return target_file

# Upload file into box
folder_id="248169789078"    #https://ibm.ent.box.com/folder/248169789078
upload_file = "/Users/suranjan/Downloads/File2UploadInBox.txt"
uploaded_file_path = upload_file_to_box(upload_file, folder_id)

# Download file from box
box_file_id = "1440341063131"   #https://ibm.ent.box.com/file/1440341063131
target_file = "/Users/suranjan/Downloads/File2DownloadFromBox1234.txt"
download_file_path = download_file_from_box(box_file_id, target_file)
