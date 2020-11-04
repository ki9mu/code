package conn

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"time"
)

func Request(url string,request_method string,data string) string{
	//log记录
	//获取当前路径
	f_path,err := os.Getwd()
	if err!=nil{
		fmt.Println("获取日志路径失败")
	}
	f_path = f_path + "/log/request.log"
	logFile, err := os.OpenFile(f_path, os.O_CREATE|os.O_RDWR|os.O_APPEND, os.ModeAppend|os.ModePerm)
	if err!=nil{
		fmt.Println(err)
		fmt.Println("日志记录错误")
		return "error"
	}
	logFile.WriteString("[info]"+time.Now().String()+"+++++"+url+"+++++"+request_method+"+++++"+data+"+++++"+"\n")


	//打印参数
	//fmt.Println(url,request_method)
	//GET请求
	if request_method == "GET"{

		//https请求
		if url[0:5]=="https"{
			tr := &http.Transport{
				MaxIdleConns:       10,
				IdleConnTimeout:    30 * time.Second,
				DisableCompression: true,
			}
			client := &http.Client{Transport: tr}
			resp, err := client.Get(url+"?"+data)
			if err !=nil{
				fmt.Println("https请求错误")
				return "error"
			}
			body,err := ioutil.ReadAll(resp.Body)
			if err !=nil{
				fmt.Println("https响应错误")
				return "error"
			}
			return string(body)

		}

		//http请求
		if url[0:5]=="http:"{
			resp,err :=http.Get(url+"?"+data)
			if err!=nil{
				fmt.Println("http请求错误")
				return "error"
			}
			body,err := ioutil.ReadAll(resp.Body)
			if err!=nil{
				fmt.Println("http响应内容错误")
				return "error"
			}
			return string(body)
		}
	}

	//POST请求
	if request_method == "POST"{

		fmt.Println("没写呢")
		//resp, err := http.PostForm(url,{"key": {"Value"}, "id": {"123"}})
		//
		//if err != nil {
		//	fmt.Println("POST请求失败")
		//	return "error"
		//}
		//
		//body, err := ioutil.ReadAll(resp.Body)
		//if err != nil {
		//	fmt.Println("获取响应内容失败")
		//	return "error"
		//}
		//
		//fmt.Println(string(body))


		//http请求
		//if url[0:5]=="http:"{
		//	resp,err :=http.Get(url+"?"+data)
		//	if err!=nil{
		//		fmt.Println("http请求错误")
		//		return "error"
		//	}
		//	body,err := ioutil.ReadAll(resp.Body)
		//	if err!=nil{
		//		fmt.Println("http响应内容错误")
		//		return "error"
		//	}
		//	return string(body)
		//}
	}

	return "error"
}
