from tkinter import *
import tkinter.messagebox as messagebox
from tkinter import filedialog

root=Tk()
lst_reg=["R0","R1","R2","R3","R4","R5","R6","R7","R8","R9","R10","R11","R12","R13","R14","R15","KBD","SCREEN","SP","LCL","ARG","THIS","THAT"]
lst2=list(range(16,16384))
clst=["A","D","M","0","1","-1"]
z=[]
var={}
val_dict={}
count=0
comp_dict={"0":'0101010',
           "1":'0111111',
           "-1":'0111010',
           "D":'0001100',
           "A":'0110000',
           "!D":'0001101',
           "!A":'0110001',
           "-D":'0001111',
           "-A":'0110011',
           "D+1":'0011111',
           "1+D":'0011111',
           "A+1":'0110111',
           "1+A":'0110111',
           "D-1":'0001110',
           "A-1":'0110010',
           "D+A":'0000010',
           "A+D":'0000010',
           "D-A":'0010011',
           "A-D":'0000111',
           "D&A":'0000000',
           "A&D":'0000000',
           "D|A":'0010101',
           "A|D":'0010101',
           "M":'1110000',
           "!M":'1110001',
           "-M":'1110011',
           "M+1":'1110111',
           "1+M":'1110111',
           "M-1":'1110010',
           "D+M":'1000010',
           "M+D":'1000010',
           "D-M":'1010011',
           "M-D":'1000111',
           "D&M":'1000000',
           "M&D":'1000000',
           "D|M":'1010101',
           "M|D":'1010101'}
dest_dict={" ":'000',
           "M":'001',
           "D":'010',
           "MD":'011',
           "DM":'011',
           "A":'100',
           "AM":'101',
           "MA":'101',
           "AD":'110',
           "DA":'110',
           "AMD":'111',
           "ADM":'111',
           "MAD":'111',
           "MDA":'111',
           "DAM":'111',
           "DMA":'111'}
jump_dict={" ":'000',
           "JGT":'001',
           "JEQ":'010',
           "JGE":'011',
           "JLT":'100',
           "JNE":'101',
           "JLE":'110',
           "JMP":'111'}

def symbols(val):
    global ins
    global z
    global val_dict
    ins2=ins.get()
    ins2=ins2[1:]
    symbols_dict={"R0":'0000000000000000',
                  "R1":'0000000000000001',
                  "R2":'0000000000000010',
                  "R3":'0000000000000011',
                  "R4":'0000000000000100',
                  "R5":'0000000000000101',
                  "R6":'0000000000000110',
                  "R7":'0000000000000111',
                  "R8":'0000000000001000',
                  "R9":'0000000000001001',
                  "R10":'0000000000001010',
                  "R11":'0000000000001011',
                  "R12":'0000000000001100',
                  "R13":'0000000000001101',
                  "R14":'0000000000001110',
                  "R15":'0000000000001111',
                  "KBD":'0110000000000000',
                  "SCREEN":'0100000000000000',
                  "SP":'0000000000000000',
                  "LCL":'0000000000000001',
                  "ARG":'0000000000000010',
                  "THIS":'0000000000000011',
                  "THAT":'0000000000000100'}
    val_dict[val]=int(symbols_dict[val])
    z.append(symbols_dict[val])

def A_Instruction():
    global ins2
    global z
    global lst_reg
    global lst2
    global val_dict
    global var
    x=ins2[1:]
    if x in lst_reg:
        symbols(ins2[1:])
    else:
        try:
            z.append('0'+f'{(int(x)):015b}')
            if ((int(x)>15 )& (int(x)<24577)):
                try:
                    val_dict[x]=int(x)
                except ValueError:
                    pass
            elif ((int(x)>=0 )& (int(x)<16)):
                val_dict[lst_reg[int(x)]]=int(x)
        except ValueError:
            if x in list(var.keys()):
                z.append(f'{var[x]:016b}')
            elif x not in val_dict.keys():     
                y=lst2.pop(0)
                z.append('0'+f'{y:015b}')
                val_dict[x]=y
            else:
                z.append('0'+f'{val_dict[x]:015b}')

def C_Instruction():
    global ins2
    global z
    global var
    global comp_dict
    global dest_dict
    global jump_dict
    o=ins2.split("=")
    try:
        p=(o.pop(1)).split(";")
        q=o+p
    except IndexError:
        p=o[0].split(";")
        q=p
    c=[];
    l=len(q)
    if l==3:
        c=('111'+comp_dict[q[1]]+dest_dict[q[0]]+jump_dict[q[2]])
    elif l==2:
        if ((len(q[1])==3)&(len(p)>1)):
            c=('111'+comp_dict[q[0]]+dest_dict[" "]+jump_dict[q[1]])
        else:
            c=('111'+comp_dict[q[1]]+dest_dict[q[0]]+jump_dict[" "])
    z.append(c)

def instruction_S(i):
    global clst
    global count
    global ins
    global ins2
    ins2=(ins.get())
    if ins2=="":
        ins2=i
    if(ins2[0]=="("):
        pass
    elif ((ins2[0]=="@")):
        A_Instruction()
    elif ((ins2[0] in clst)):
        C_Instruction()
    else: 
        messagebox.showerror("warning","ERROR IN INPUT")

def ins_V(j):
    global count
    global var
    if(j[0]=="("):
        var[j[1:-1]]=count
    else:
        count=count+1

def writefile():
    global z
    global var
    global filename
    fn2=filename.split(".")
    filename2=""
    filename2=filename2+fn2[0]+".hack"
    file2=open(filename2,"w")
    for j in z:
        file2.writelines((j)+"\n")
    messagebox.showinfo("Information", "result file is stored in:"+filename2)
    file2.close()

def browseFiles():
    global filename
    global count
    filename = filedialog.askopenfilename(initialdir = "/",title = "Select a File",filetypes = (("Text files","*.txt*"),("all files","*.*")))
    file1 = open(filename, "r")
    code=(file1.readlines())
    code=[s.replace('\n','') for s in code]
    code=[s.replace('\t','') for s in code]
    code=[s.split("\\")[0] for s in code]
    code=[s.split("//")[0] for s in code]
    code=[s.replace(" ","")for s in code]
    code = [x for x in code if x != '']
    for i in code:
        ins_V(i)
    count=0;
    for i in code:
        instruction_S(i)
    writefile()

def b4instruction():
    global var
    global count
    global z
    global val_dict
    var={}
    count=0
    z=[]
    val_dict={}
    browseFiles()

def instruction_b():
    global ins
    global z
    z=[]
    ins2=ins.get()
    instruction_S(ins2)
    information=z
    if z!=[]:
        messagebox.showinfo("Answer", information)

root.title("Assembler")
root.geometry("500x300")
root.configure(bg="#FFFFFF")
frame1 = Frame(root,background="#FFFFFF")
lbl1= Label(frame1, text = "Assembler", font=('Arial',25,'bold'),bg="#FFFFFF",fg='#000FFF')
lbl1.pack()
frame1.pack()
frame2=Frame(root,background="#FFFFFF")
lbl2=Label(frame2,text="Enter instruction",background="#FFFFFF")
lbl2.grid(row=0,column=0,padx=25,sticky='w')
global ins
ins=StringVar()
ins=Entry(frame2, textvariable=ins,width=20, font=('calibre',10,'normal'),relief='flat',highlightthickness=2,highlightcolor="#4169E1")
ins.grid(row=0,column=1,padx=25,sticky='w')
btn1 = Button(frame2,command=instruction_b, text="Submit",relief='flat',font=('Ariel',8,'bold'),width=7,height=1,bg="#000FFF",fg="#FFFFFF",activebackground="#FFFFFF",activeforeground="#000FFF")
btn1.grid(row=5,column=0,padx=28,sticky='w',columnspan=2,pady=20)
btn2 = Button(frame2,command=b4instruction, text="open file",relief='flat',font=('Ariel',8,'bold'),width=7,height=1,bg="#000FFF",fg="#FFFFFF",activebackground="#FFFFFF",activeforeground="#000FFF")
btn2.grid(row=5,column=1,padx=28,sticky='w',columnspan=2,pady=20)
frame2.pack()
root.mainloop()

