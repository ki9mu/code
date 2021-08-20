# -*- coding: utf-8 -*-
# @Time : 2021/8/19 11:49
# @Author : ki9mu
# @File : translate.py
# @Software: PyCharm
import os
import yaml
import requests


def read_yaml():
    path = "cves"
    dict_file = []
    for dir in os.listdir(path):
        for yaml_file in os.listdir("cves/" + dir):
            dict_file.append("cves/" + dir + "/" + yaml_file)
            # print(yaml_file)
    return dict_file


def get_filedata(file_path):
    f = open(file_path, encoding="utf-8")
    data = yaml.safe_load(f)
    return data


def detail_filedata(data):
    # info
    data_info: dict = data.get("info")

    name = data_info.get("name") or None
    reference = data_info.get("reference") or None
    tags = data_info.get("tags") or None
    severity = data_info.get("severity") or None
    cve = data.get("id")
    aqk_data:dict = anquanke_req(cve)
    # print(reference, tags, severity)
    # print(type(reference), type(tags), type(severity))
    info = {"name": aqk_data.get("name"), "author": "ki9mu","description":aqk_data.get("description"),
            "reference": reference, "vuln_type": "",
            "app_name": "", "tags": tags, "severity": severity, "cve": cve}
    #print(info)

    # dir
    dir_list = ["/"]

    # request
    data_req:dict = data.get("requests")
    http = []
    if data_req[0].get("raw") == None:
        for req in data_req:
            request = {}
            request["method"] = req.get("method")
            request["path"] = req.get("path")
            request["data"] = req.get("body")
            request["headers"] = req.get("headers")

            machers = req.get("matchers")
            #print(machers)
            response = {}
            for macher in machers:

                if macher.get("type") == "status":
                    response["status_code"] = macher.get("status")
                else:
                    #print(macher.get("type"))
                    part = macher.get("part") or "body"
                    if macher.get("type") == "word":
                        response[part] = {"content":macher.get("words")}
                    if macher.get("type") == "regex":
                        response[part] = {"regex": macher.get("regex")}

            # print(response)
            http.append({"request":request,"response":response})
    else:
        if data_req != None and len(data_req) == 1:
            entity = {}
            request_data = data_req[0].get("raw")[0].split("\n")
            req_data = [x for x in request_data if x]
            #print(req_data[-1])

            # get method
            method = req_data[0].split(" ")[0]
            if method != "GET":
                entity["method"] = method
                # get body
                entity["body"] = req_data[-1]
            else:
                entity["method"] = "GET"

            # get url
            url = req_data[0].split(" ")[1]
            entity["path"] = url

            # get header
            ignore_list = ["Content-Length", "Accept-Language", "Connection", "{{Hostname}}"]
            headers = {}
            if entity.get("method") == "GET" or entity.get("method") == None:
                req_data.append("")
            #print(req_data[1:-1])
            for i in req_data[1:-1]:
                for ignore in ignore_list:
                    if ignore in i:
                        break
                else:
                    header = i.split(":", 1)
                    headers[header[0]] = header[1]
                    entity["headers"] = headers
            #print(entity)

            machers = data_req[0].get("matchers")
            response = {}
            for macher in machers:
                part = macher.get("part") or "body"
                if macher.get("type") == "word":
                    response[part] = {"content": macher.get("words")}
                if macher.get("type") == "regex":
                    response[part] = {"regex": macher.get("regex")}
            #print(response)
            http.append({"request":entity,"response":response})
        else:
            print(data.get("id"))

    new_data = {"info":info,"dir_list":dir_list,"http":http}

    return new_data


def anquanke_req(cve) -> dict:
    url = "https://api.anquanke.com/data/v1/search/vul?s={cve}&c=&field=&start=&end=&c=&platform=".format(cve=cve)
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}
    response = requests.get(url=url, headers=header)
    response_data: dict = response.json()
    #print(response_data)
    if response_data.get("success") == "true":
        for item in response_data.get("data"):
            if item.get("cve") == cve:
                return {"name": item.get("name"), "description": item.get("description")}
    return {"name": "", "description": ""}


def file_write(data,path):
    new_filepath = "vulnerabilities/cve" + path[4:]
    #print(new_filepath)
    with open(new_filepath,'w') as f:
        yaml.safe_dump(data,f)


def main():
    file_list = read_yaml()
    for file_path in file_list:
        try:
            old_data: dict = get_filedata(file_path)
            new_data: dict = detail_filedata(old_data)
            #print(new_data)
            file_write(new_data,file_path)
            # exit(0)
        except:
            continue
            print(file_path)
            exit(0)


if __name__ == '__main__':
    main()
    #anquanke_req("CVE-2005-2428")
