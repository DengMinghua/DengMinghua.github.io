from flask import Flask, request, jsonify, render_template
import pymongo 
app = Flask("__name__")

@app.route('/upload_contact', methods=["POST"])
def upload():
    client = pymongo.MongoClient()
    db = client["contactDb"]
    contactCol = db.contactCol    
    jsonInfo = request.json
    print(jsonInfo["uuid"])
    contactCol.update({'name':jsonInfo["name"]},
                      {$set:{"uuid":jsonInfo["uuid"], "name":jsonInfo["name"],"phone":jsonInfo["phone"],"avatar":jsonInfo["avatar"]}},
                      {upsert:true})
    #contactCol.insert_one({"uuid":jsonInfo["uuid"], "name":jsonInfo["name"],"phone":jsonInfo["phone"],"avatar":jsonInfo["avatar"]})
    return "Successed"

@app.route('/download_contact', methods=['GET'])
def download():
    uuid = str(request.args.get('uuid'))
    client = pymongo.MongoClient()
    db = client["contactDb"]
    contactCol = db.contactCol
    resultDic = {}
    cursor = contactCol.find({"uuid":uuid})
    cnt = 0
    for doc in cursor:
        resultDic[str(cnt)] = {"name":doc["name"],"phone":doc["phone"],"avatar":doc["avatar"]}
        cnt += 1
    # resultDic['0'] = {"name":"Gakki", "phone":"18819253703", "avatar":"gakki.jpg"}
    # resultDic['1'] = {"name":"Kobe Byrant", "phone":"18819224735", "avatar":"kobe.jpg"}
    # resultDic['2'] = {"name":"Non", "phone":"18829914433","avatar":"non.jpg"}
    # resultDic['3'] = {"name":"Satomi Ishihara", "phone":"19321434233","avatar":"satomi.jpg"}
    return jsonify(resultDic)
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
