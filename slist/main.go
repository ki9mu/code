package main

import (
	"fmt"
	"slist/core"
)


func main() {
	//读取url文件
	//[]string
	//
	url_data := core.Read_file("/file/url_data.txt")
	//fmt.Println(url_data)
	//fmt.Println("v1 type:", reflect.TypeOf(url_data))
	//
	//输入链接
	//slist("http://www.bilibili.com")
	//测试所有链接
	for i,s := range url_data{
		//判断是否为正常链接
		if len(s)>2&&s[0:4]=="http"{
			core.Slist(s)
			fmt.Println(i,s)
		}
	}
	//url_list := core.Read_file("/file/url_data.txt")
	//fmt.Println(url_list)
	//for i,url:= range url_list{
	//	fmt.Println(i,url)
	//	core.Spider(url)
	//}
}