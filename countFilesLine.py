#encoding=utf-8
import os
class CountLinesOfValuableCode(object):
    def __init__(self,dirsPath,choice,*suffix):
        '''
        :param  dirs_list  type： list 统计有效代码行的文件路径
        :param  files_list  type：list 所有需要被统计的文件路径
        :param  choice  type：number 统计或者不统计的后面的后缀名元组
        :param  suffix  type：tuple 不执行的文件后缀名
        :param  valuable_lines_number  type：number 有效代码行数
        :param  unvaluable_lines_number  type：number 无效代码行数
        '''
        self.dirsPath=dirsPath
        self.choice = choice
        self.suffix=suffix
        self.files_list=[]
        self.valuable_lines_number=0
        self.unvaluable_lines_number=0

    def LookForFile(self):
        try:
            if os.path.exists(self.dirsPath) and os.path.isdir(self.dirsPath):
                for rootpath,dirs,files in os.walk(self.dirsPath):          #递归遍历所有文件及文件夹
                    for file in files:
                        file_name_path = os.path.join(rootpath, file)       #拼接完整的文件路径
                        if self.choice==0:
                            if os.path.isfile(file_name_path) and os.path.splitext(file_name_path)[1] not in self.suffix:  #排除日志文件等
                                self.files_list.append(file_name_path)
                        else:
                            if os.path.isfile(file_name_path) and os.path.splitext(file_name_path)[1] in self.suffix:  #排除日志文件等
                                self.files_list.append(file_name_path)
                print("需要统计行数的文件路径是：%s"%self.files_list)
                print("需要统计行数的文件数量是：%s"%len(self.files_list))
                return (self.files_list,len(self.files_list))
            elif os.path.exists(self.dirsPath) and os.path.isfile(self.dirsPath):
                self.files_list.append(self.dirsPath)
                return (self.files_list,len(self.files_list))
            else:
                print("输入的路径'%s'不存在！！！"%self.dirsPath)
                return (self.files_list,len(self.files_list))
        except Exception as e:
            print(e)

    def CountCodeLines(self):
        for file_path in self.files_list:
            swicth=0                    #0表示非文档说明，1表示开始文档说明
            if os.path.splitext(file_path)[1]==".py":           #判断是python文件
                with open(file_path,"r",encoding="utf-8") as fq:
                    lines_list=fq.readlines()                   #读取文件所有内容，并生成list
                    for line in lines_list:
                        if swicth==0 and line.strip()=="":      #非文档说明的空行
                            self.unvaluable_lines_number+=1
                        elif swicth==0 and line.lstrip().startswith("#"):      #非文档说明的注释
                            self.unvaluable_lines_number += 1
                        elif swicth==0 and (line.lstrip().startswith('"""') or line.lstrip().startswith("'''")):  #文档注释开始
                            self.unvaluable_lines_number += 1
                            swicth=1
                        elif swicth==1 and (line.rstrip().endswith('"""') or line.rstrip().endswith("'''")):  #文档注释结束
                            swicth = 0
                            self.unvaluable_lines_number += 1
                        elif swicth==1 and not (line.lstrip().startswith('"""') or line.lstrip().startswith("'''"))\
                                and not (line.rstrip().endswith('"""') or line.rstrip().endswith("'''")):   #文档注释内容
                            self.unvaluable_lines_number += 1
                        else:                                                           #有效代码行
                            self.valuable_lines_number+=1
            elif  os.path.splitext(file_path)[1]==".java":           #判断是java文件
                with open(file_path,"r",encoding="utf-8") as fq:
                    lines_list=fq.readlines()                   #读取文件所有内容，并生成list
                    for line in lines_list:
                        if swicth==0 and line.strip()=="":      #非文档说明的空行
                            self.unvaluable_lines_number+=1
                        elif swicth==0 and line.lstrip().startswith("//"):      #非文档说明的注释
                            self.unvaluable_lines_number += 1
                        elif swicth==0 and (line.lstrip().startswith('/**') or line.lstrip().startswith("/*")):  #文档注释或者多行注释开始
                            self.unvaluable_lines_number += 1
                            swicth=1
                        elif swicth==1 and line.rstrip().endswith('*/'):  #文档注释或者多行注释结束
                            swicth = 0
                            self.unvaluable_lines_number += 1
                        elif swicth==1 and not (line.lstrip().startswith('/**') or line.lstrip().startswith("/*"))\
                                and not (line.rstrip().endswith('*/') or line.rstrip().endswith("*/")):   #文档注释内容
                            self.unvaluable_lines_number += 1
                        else:                                                           #有效代码行
                            self.valuable_lines_number+=1
            else:
                with open(file_path,"r",encoding="utf-8") as fq:
                    lines_list=fq.readlines()                   #读取文件所有内容，并生成list
                    for line in lines_list:
                        if line.strip()=="":      #空行
                            self.unvaluable_lines_number+=1
                        else:                                                           #有效代码行
                            self.valuable_lines_number+=1

        print("有效行数是%s"%self.valuable_lines_number)
        print("无效行数是%s"%self.unvaluable_lines_number)
        return (self.valuable_lines_number,1,self.unvaluable_lines_number)







if __name__ =="__main__":
    counter=CountLinesOfValuableCode(r"E:\whiteMouseProduct\CountFilesLine\2020.log",1,".log",".py",".java")
    counter.LookForFile()
    counter.CountCodeLines()

