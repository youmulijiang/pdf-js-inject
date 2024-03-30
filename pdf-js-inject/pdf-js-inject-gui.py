import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.font import Font
import os

try:
    from pypdf import PdfReader,PdfWriter
except ImportError as e:
    messagebox.showerror("运行失败","没有下载依赖项")
    print(e)
    print("正在下载工具依赖项")
    os.system("pip install pypdf")

def pdf_js_inject(template_file_path,save_path,js_code:str=None,js_file:str=None,encrypt_password=None):
    output_pdf = PdfWriter()
    temp_pdf = PdfReader(template_file_path)

    for i in range(len(temp_pdf.pages)):
        page = temp_pdf.pages[i]
        output_pdf.add_page(page)

    if encrypt_password is not None:
        output_pdf.encrypt(encrypt_password,algorithm='AES-256')
        # print("encrypt success")
    try:
        with open(save_path,'wb') as evil_pdf:
            if js_code is not None:
                output_pdf.add_js(js_code)
            if js_file is not None:
                with open(js_file,'r') as js:
                    output_pdf.add_js(js.read())
            output_pdf.write(evil_pdf)
        
        messagebox.showinfo("注入成功","注入成功")
    except:
        messagebox.showerror("注入失败","注入失败")

    # print("\npdf inject js success\n")

class Application(tk.Tk):
    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use) 

        self.custom_font = Font(family="Microsoft YaHei UI", size=11)
        self.option_add("*Font",self.custom_font)

        self.menu_bar = tk.Menu(self)
        sub_about_menu = tk.Menu(self.menu_bar,tearoff=0)
        sub_about_menu.add_cascade(label="作者",command=lambda:messagebox.showinfo("作者","柚木梨酱"))
        sub_about_menu.add_cascade(label="版本",command=lambda:messagebox.showinfo("版本","pdf-js-inject-gui:1.0"))
        sub_about_menu.add_cascade(label="退出",command=lambda:exit(1))
        self.tab = self.menu_bar.add_cascade(label="about",menu=sub_about_menu)

        self.grid_columnconfigure(index=1,pad="20")


        self.config(menu=self.menu_bar)   

        self.cheak_var = tk.IntVar(value=0) 
        self.pdf_encrypt_passwd = None

        self.labal_1 = ttk.Label(self,text="请输入pdf模板路径:")
        self.entry_1 = ttk.Entry(self)
        self.labal_2 = ttk.Label(self,text="请输入pdf保存路径:")
        self.entry_2 = ttk.Entry(self)
        self.button_1 = ttk.Button(self,text="请选择pdf模板文件的路径",command=self.button_get_file_path)
        self.button_2 = ttk.Button(self,text="请选择保存pdf的路径",command=self.button_save_file_path)
        self.checkbutton = ttk.Checkbutton(self,text="加密pdf",command=self.encrypt_pdf,variable=self.cheak_var)
        # self.message = tk.Message(self,width=300,bg="red")
        self.text = tk.Text(self,width="52",height="10")
        self.text.insert("1.0","请输入要注入的js")

        def focusin(event):
            if self.text.get('1.0','end-1c') == "请输入要注入的js":
                self.text.delete("0.0",tk.END)
            
        def focusout(event):
            if self.text.get('1.0','end-1c') == "":
                self.text.insert("0.0","请输入要注入的js")

        self.text.bind("<FocusIn>",focusin)
        self.text.bind("<FocusOut>",focusout)

        self.button_3 = ttk.Button(self,text="请选择想输入的js文件",command=self.inject_js_file)
        self.button_4 = ttk.Button(self,text="注入js",command=self.start_inject_js)
        

        self.labal_1.grid(row=0,column=0,sticky="w",pady="10")
        self.labal_2.grid(row=1,column=0,sticky="w")
        self.entry_1.grid(row=0,column=1,sticky="w")
        self.entry_2.grid(row=1,column=1,sticky="w")
        self.button_1.grid(row=0,column=2,sticky="w")
        self.button_2.grid(row=1,column=2,sticky="w")
        self.checkbutton.grid(row=2,column=0,sticky="w")
        # self.text.grid(row=3,column=0,sticky="nsew")

        self.text.place(x=10,y=110)
        self.button_3.place(x=10,y=320)
        self.button_4.place(x=10,y=360)

    def button_get_file_path(self):
        file_name = filedialog.askopenfilename(title="请选择pdf模板路径",filetypes=[('PDF file','*.pdf')])
        self.entry_1.delete(0,tk.END)
        self.entry_1.insert(0,file_name)

    def button_save_file_path(self):
        file_name = filedialog.asksaveasfilename(title="请选择pdf保存路径",filetypes=[("PDF file","*.pdf")],defaultextension=".pdf")
        self.entry_2.delete(0,tk.END)
        self.entry_2.insert(0,file_name)

    def encrypt_pdf(self):
        if self.cheak_var.get() == 1:
            self.encrypt_pdf_entry = ttk.Entry(self)
            self.encrypt_pdf_entry.grid(row=2,column=1)
            self.encrypt_pdf_entry.insert(0,"请输入密码")

            def focusin(event):
                if self.encrypt_pdf_entry.get() == "请输入密码":
                    self.encrypt_pdf_entry.delete(0,tk.END)
                                   
            def focusout(event):
                if self.encrypt_pdf_entry.get() == "":
                    self.encrypt_pdf_entry.insert(0,"请输入密码")
                else:
                    self.pdf_encrypt_passwd = self.encrypt_pdf_entry.get()

            self.encrypt_pdf_entry.bind("<FocusIn>",focusin)
            self.encrypt_pdf_entry.bind("<FocusOut>",focusout)
            
            
        else:
            if hasattr(self, "encrypt_pdf_entry"):  # 检查组件是否存在
                self.encrypt_pdf_entry.grid_forget()
                self.pdf_encrypt_passwd = None
    
    def inject_js_file(self):
        
        js_file_path = filedialog.askopenfilename(filetypes=[("js_inject_file",["*.js","*.txt"])])
        with open(js_file_path,"r",encoding="utf-8") as js_file:
            js_code = js_file.read()
            if self.text.get("1.0","end-1c") != "":
                self.text.delete("1.0",tk.END)
            if self.text.get("1.0","end-1c") == "":
                self.text.insert("1.0",js_code)

    def start_inject_js(self):
        template_pdf = self.entry_1.get()
        save_path = self.entry_2.get()
        js_code = self.text.get("0.0","end-1c")
        pdf_js_inject(template_pdf,save_path,encrypt_password=self.pdf_encrypt_passwd,js_code=js_code)
        # print("passwd:",self.pdf_encrypt_passwd)
        


if __name__ == '__main__':
    app = Application()
    app.title("pdf-js-inject-gui")
    app.wm_geometry('500x400+100+100')
    app.wm_iconphoto(False,tk.PhotoImage(file=r'pdf-js-inject\icon\hacker.png'))
    try:
        app.mainloop()
    except KeyboardInterrupt:
        os._exit(1)
        pass