from github import Github
import requests
import base64
import json
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin

# 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
app = Flask(__name__)
CORS(app)

g = Github("AshishBotMantra", "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")
repo = g.get_user().get_repo('file_upload_to_git_repo')
all_files = []
contents = repo.get_contents("")
while contents:
    file_content = contents.pop(0)
    if file_content.type == "dir":
        contents.extend(repo.get_contents(file_content.path))
    else:
        file = file_content
        all_files.append(str(file).replace('ContentFile(path="','').replace('")',''))
print(all_files)

def uploading_to_github(fileName):
    with open(fileName, 'r') as file:
        content = file.read()
    git_prefix = ''
    git_file = git_prefix + fileName
    try:
        if git_file in all_files:
            contents = repo.get_contents(git_file)
            repo.update_file(contents.path, "committing files", content, contents.sha, branch="main")
            print(git_file + ' UPDATED')
        else:
            repo.create_file(git_file, "committing files", content, branch="main")
            print(git_file + ' CREATED')
    except Exception as e:
        print(str(e))

@app.route('/insert_json',methods=['POST'])
@cross_origin(origin='*')
def get_json():
    password = request.json['password']
    fileType = request.json['fileType']
    fileName = request.json['fileName']
    filePath = request.json['filePath']
    file_content = filePath
    # print(file_content)
    encoded = base64.b64decode(file_content)
    try:
        with open(fileName,'w') as f:
            f.write(str(encoded.decode('unicode_escape').encode('utf-8')))
    except Exception as e:
        print(str(e))
    uploading_to_github(fileName)
    return jsonify({"message":"file created"})



if __name__ == '__main__':
    # CORS(app,resources={r"/*":{"origin":"*"}})
    app.run(debug=True)