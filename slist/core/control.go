package core

import (
	"fmt"
	"io/ioutil"
	"os"
	"strings"
	"regexp"
	"time"
	"net/http"
)


//读文件
func Read_file(filepath string)  ([]string){
	//获取当前路径
	f_path,err := os.Getwd()
	if err!=nil{
		fmt.Println("文件路径失败")
	}

	//绝对路径 = 当前路径+相对路径
	f_path = f_path + filepath
	//fmt.Println(f_path)

	//根据绝对路径打开文件
	f, err := os.Open(f_path)
	if err != nil {
		fmt.Println("read file fail", err)
		return []string{"error"}
	}

	//读取文件内容
	fd, err := ioutil.ReadAll(f)
	if err != nil {
		fmt.Println("read to fd fail", err)
		return []string{"error"}
	}


	return strings.Split(string(fd),string([]byte{13,10}))
}

//写文件
func Write_file(filepath string,data string) bool {
	f_path, err := os.Getwd()
	if err != nil {
		fmt.Println("文件路径失败")
		return false
	}
	f_path = f_path + filepath
	pathFile, err := os.OpenFile(f_path, os.O_CREATE|os.O_RDWR|os.O_APPEND, os.ModeAppend|os.ModePerm)
	if err != nil {
		fmt.Println(err)
		fmt.Println("文件记录错误")
		return false
	}
	pathFile.WriteString(data + "\n")
	pathFile.Close()
	return true
}

//对url页面提取路径
func Slist(url string) {

	//获取页面详情
	data := Request(url,"GET","")
	//过滤路径
	href_reg := regexp.MustCompile(`href=".*?"`)
	http_reg := regexp.MustCompile(`http://.*?"`)
	https_reg := regexp.MustCompile(`https://.*?"`)
	src_reg := regexp.MustCompile(`src=".*?"`)
	//拆分路径名&&写入文件
	href_data := href_reg.FindAllString(data, -1)
	http_data := http_reg.FindAllString(data, -1)
	https_data := https_reg.FindAllString(data, -1)
	src_data := src_reg.FindAllString(data, -1)
	all_data := [][]string{href_data,http_data,https_data,src_data}


	//写入文件
	f_path,err := os.Getwd()
	if err!=nil{
		fmt.Println("文件路径失败")
	}
	f_path = f_path + "/file/path.txt"
	pathFile, err := os.OpenFile(f_path, os.O_CREATE|os.O_RDWR|os.O_APPEND, os.ModeAppend|os.ModePerm)
	if err!=nil{
		fmt.Println(err)
		fmt.Println("文件记录错误")
	}
	for j:=0;j<4;j++ {
		for _, s := range all_data[j] {
			path := strings.Split(s,"/")
			for _,pure_data := range path{
				//fmt.Println(pure_data)
				//如果包含特殊字符，抛弃掉
				if strings.ContainsAny(pure_data, ",|\"./:"){
					continue
				}
				if pure_data == ""{
					continue
				}
				pathFile.WriteString(pure_data+"\n")
			}

		}
	}
	pathFile.Close()
}

//web请求
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

//网页爬虫
func Spider(url string)  {
	//fmt.Println("spider:",url)
	//请求页面
	resp_data := Request(url,"GET","")

	//提取其中跳转链接
	href_reg := regexp.MustCompile(`(a href=".*?)"`)
	http_data := href_reg.FindAllString(resp_data, -1)

	//遍历跳转链接
	for _,jmp := range http_data{
		//如果为相对路径


		//若#结束当前url
		if jmp[8:9] == "#"{
			continue
		}

		if jmp[0:12] != "a href=\"http"{
			urljmp := url + jmp[8:]
			fmt.Println(jmp,jmp[8:])
			Write_file("/file/url.txt",urljmp)
			if urljmp == url{
				break
			}
			Spider(urljmp)
		}
		if jmp[0:12] == "a href=\"http"{
			urljmp := jmp[8:]
			fmt.Println(jmp,urljmp)
			Write_file("/file/url.txt",urljmp)
			if urljmp == url{
				break
			}
			Spider(urljmp)
		}


	}


}
