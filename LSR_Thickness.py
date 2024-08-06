
from tkinter import *
from turtle import end_fill, pos, width
from matplotlib.pyplot import get
from requests import delete
import scipy as sp
import pandas as pd
from datetime import datetime
import time
from tokenize import Double
from turtle import bgcolor
from tkinter import messagebox

ym = time.strftime("%D")
t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)

def on_click():
    sc_min,sc_max=(specinput.get()).split("-")
    side_input = side.get()
    sc_min = float(sc_min)/1000
    sc_max = float(sc_max)/1000
    n1=float(input1.get())
    n2=float(input2.get())
    n3=float(input3.get())
    n4=float(input4.get())
    n5=float(input5.get())
    n6=float(input6.get())
    n7=float(input7.get())
    n8=float(input8.get())
    n9=float(input9.get())
    n10=float(input10.get())
    n11=float(input11.get())
    n12=float(input12.get())
    cpk = 0
    dt = datetime.now().strftime('%Y-%m-%dT %H: %M: %S')
    df=pd.DataFrame([n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11,n12])
    df_output = pd.DataFrame()
    df.columns = ['input']
    df=df.query('input > 0')
    
    print(df)
    print(sc_max,sc_min)
    df = df.reset_index()
    del df['index']
    avg_value=sp.mean([df])
    print('avg=',avg_value)
   
    #avg_value=sp.mean([n1,n2,n3,n4,n5,n6])
    sigma_value=sp.std([df])
    cpu=float((sc_max-avg_value)/(3*sigma_value))
    cpl=float((avg_value-sc_min)/(3*sigma_value))
    if cpu < cpl:
        cpk=cpu
    elif cpu>cpl:
        cpk = cpu
    print(cpu,cpl,cpk)
    map =(pos_scan.get()).split(";")
    if len(map[0]) == 9:
        prd=map[2]
        lot_no = map[0]
    else:
        prd = map[1]
        lot_no = map[2].split(",")
        print(lot_no)
    ##concat lot no
    # df_lotno = pd.DataFrame()
    # df_lotno['lot_no'] = lot_no    
        

    df_output['side']=[side_input]
    df_output['product_name'] = [prd]
    
    df_output['spec_min'] = sc_min
    df_output['spec_max'] = sc_max

    df_output['average'] = avg_value
    df_output['cpk'] = cpk
    #Display
    avg_result.configure(text=f'{avg_value:.2f}') 
    cpk_result.configure(text=f'{cpk:.2f}')
    # df_output = df_output.reset_index()
    # del df_output['index']
    print(df_output)
    print(df)
    # df_output = pd.concat([df_lotno,df_output],axis=1)
    dt = pd.concat([df,df_output],axis=1)
    print(dt)
    #Save to csv
    if len(map[0]) == 9:
        dt.to_csv(r'D:\Thickness'+f"\{prd}"+'_'+lot_no+'_'+side_input+'.csv',index=None)
    else:
        dt.to_csv(r'D:\Thickness'+f"\{prd}"+'_'+map[2]+'_'+side_input+'.csv',index=None)
        
    color_zone= ''
    if avg_value >= sc_max:
        color_zone='red' 
    elif avg_value <= sc_min:
        color_zone='red' 
    else:
        color_zone='lime'
    avg_result['bg']=color_zone  

    color_zone_cpk= ''
    if cpk >= 1.33:
        color_zone_cpk='lime' 
    else:
        color_zone_cpk='red'
    cpk_result['bg']=color_zone_cpk      
    messagebox.showinfo("saved","already saved")

def cancel():
    pd_name.configure(text="", bg=None)  
    lot.configure(text="", bg=None)  
    min_output.configure(text="", bg=None)  
    max_output.configure(text="", bg=None)  
    op1.configure(text="", bg='#f0f0f0')
    op2.configure(text="", bg='#f0f0f0')        
    op3.configure(text="", bg='#f0f0f0')    
    op4.configure(text="", bg='#f0f0f0')  
    op5.configure(text="", bg='#f0f0f0')  
    op6.configure(text="", bg='#f0f0f0')
    op7.configure(text="", bg='#f0f0f0')
    op8.configure(text="", bg='#f0f0f0')        
    op9.configure(text="", bg='#f0f0f0')    
    op10.configure(text="", bg='#f0f0f0')  
    op11.configure(text="", bg='#f0f0f0')  
    op12.configure(text="", bg='#f0f0f0')    
    for widget in root.winfo_children():
        if isinstance(widget, Entry):  # If this is an Entry widget 
            widget.delete(0,'end') 
            widget.insert(0,0.0)
    spec_input.delete(0,'end')   
    side.delete(0,'end')
    pos.delete(0,'end')     
    avg_result.configure(text="", bg='#f0f0f0')  
    cpk_result.configure(text="", bg='#f0f0f0')  
    pos.focus()
   
    pass


root=Tk()
root.option_add('*font','impack 16') 
root.title("Thickness")
# Parameter input
class Clock:
    def __init__(self):
        self.time1 = ''
        self.time2 = time.strftime('%H:%M:%S')
        self.mFrame = Frame()
        self.mFrame.grid(row=1,column=3,pady=5) 

        self.watch = Label(self.mFrame, text=self.time2)
        self.watch.pack()

        self.changeLabel() #first call it manually

    def changeLabel(self): 
        self.time2 = time.strftime('%H:%M:%S')
        self.watch.configure(text=self.time2)
        self.mFrame.after(200, self.changeLabel) #it'll call itself continuously

C=Clock()

spec=DoubleVar()

Label(root,text='POS Scan').grid(row=0,column=0,padx=5,pady=5)
###
pos_scan = StringVar()

def split_pos(event):
    input=pos_scan.get()
    map = input.split(";")
    if len(map[0]) == 9:
        pd_name.configure(text=map[2])
        lot.configure(text=map[0])
    else:
        pd_name.configure(text=map[1])
        lot.configure(text=map[2])
        
pos = Entry(root,textvariable=pos_scan,width=10,justify='right')
pos.grid(row=0,column=1)
pos.bind("<Key>",split_pos)
##showsplit
Label(root,text='PRD Name').grid(row=1,column=0,padx=5)
pd_name=Label(root)
pd_name.grid(row=1,column=1,padx=5)
Label(root,text='Lot No').grid(row=2,column=0,padx=5)
lot = Label(root)
lot.grid(row=2,column=1,padx=5,pady=7)
min=Label(root,text='Min-spec').grid(row=5,column=0,padx=5)
min_output = Label(root)
min_output.grid(row=5,column=1,padx=5)
max=Label(root,text='Max-spec').grid(row=5,column=2,padx=5)
max_output = Label(root)
max_output.grid(row=5,column=3,padx=5)

#section2
# input
##input side
Label(root,text='Side').grid(row=3,column=0,)
side = Entry(root,textvariable=StringVar(),width=10,justify='right')
side.grid(row=3,column=1)

##specinput
Label(root,text='Spec').grid(row=4,column=0,)
specinput = StringVar()
def inputspec(var, index, mode):
  input=specinput.get()
  if len(input)>=5:
    sc_min,sc_max=(specinput.get()).split("-")
    minn=str(float(sc_min)/1000)
    maxx= str(float(sc_max)/1000)
    print(type(maxx))
    max_output.configure(text=maxx)
    min_output.configure(text=minn)
    input1.focus()
    input1.delete(0,'end')
specinput.trace_variable("w", inputspec)
spec_input=Entry(root,textvariable=specinput,width=10,justify='right')
spec_input.grid(row=4,column=1,padx=5) 
##input1
Label(root,text='input 1').grid(row=6,column=0,padx=5)
ip1=StringVar()
def checkresult1(var, index, mode):
    input = ip1.get()
    inputs=specinput.get()
    min,max = inputs.split("-")
    if len(input)==5:
        input= float(input)
        if input == 0:
            op1.configure(text='',bg='#f0f0f0')
        elif float(input) > float(max)/1000 or float(input)< float(min)/1000:
            op1.configure(text='NG',bg='red')
            input2.focus()
            input2.delete(0,'end')
        else:
            op1.configure(text='PASS',bg='green')
            input2.focus()
            input2.delete(0,'end')

ip1.trace_variable('w',checkresult1)
input1 = Entry(root,textvariable=ip1,width=10,justify='right')
input1.grid(row=6,column=1,padx=5) 
##input2
ip2=StringVar()
Label(root,text='input 2').grid(row=7,column=0,padx=5)
def checkresult2(var, index, mode):
    input = ip2.get()
    print(len(f'{input}'))
    if len(input)==5:
        inputs=specinput.get()
        min,max = inputs.split("-")
        input= float(input)
        if input == 0:
            op2.configure(text='',bg='#f0f0f0')
        elif float(input) > float(max)/1000 or float(input)< float(min)/1000:
            op2.configure(text='NG',bg='red')
            input3.focus()
            input3.delete(0,'end')
        else:
            op2.configure(text='PASS',bg='green')
            input3.focus()
            input3.delete(0,'end')
ip2.trace_variable('w',checkresult2)
input2=Entry(root,textvariable=ip2,width=10,justify='right')
input2.grid(row=7,column=1,padx=5) 
##input3
ip3 = StringVar()
def checkresult3(var, index, mode):
    input = ip3.get()
    print(len(f'{input}'))
    if len(input)==5:
        input= float(input)
        inputs=specinput.get()
        min,max = inputs.split("-")
        if input == 0:
            op3.configure(text='',bg='#f0f0f0')
        elif float(input) > float(max)/1000 or float(input)< float(min)/1000:
            op3.configure(text='NG',bg='red')
            input4.focus()
            input4.delete(0,'end')
        else:
            op3.configure(text='PASS',bg='green')
            input4.focus()
            input4.delete(0,'end')
   
ip3.trace_variable('w',checkresult3)
Label(root,text='input 3').grid(row=8,column=0,padx=5)
input3= Entry(root,textvariable=ip3,width=10,justify='right')
input3.grid(row=8,column=1,padx=5) 
##input4
ip4 = StringVar()
def checkresult4(var, index, mode):
    input = ip4.get()
    print(len(f'{input}'))
    if len(input)==5:
        inputs=specinput.get()
        min,max = inputs.split("-")
        input= float(input)
        if input == 0:
            op4.configure(text='',bg='#f0f0f0')
        elif float(input) > float(max)/1000 or float(input)< float(min)/1000:
            op4.configure(text='NG',bg='red')
            input5.focus()
            input5.delete(0,'end')
        else:
            op4.configure(text='PASS',bg='green')
            input5.focus()
            input5.delete(0,'end')
Label(root,text='input 4').grid(row=9,column=0,padx=5)
ip4.trace_variable('w',checkresult4)
input4=Entry(root,textvariable=ip4,width=10,justify='right')
input4.grid(row=9,column=1,padx=5)
##input5
ip5 = StringVar()
Label(root,text='input 5').grid(row=10,column=0,padx=5)
def checkresult5(var, index, mode):
    input = ip5.get()
    print(len(f'{input}'))
    if len(input)==5:
        inputs=specinput.get()
        min,max = inputs.split("-")
        input= float(input)
        if input == 0:
            op5.configure(text='',bg='#f0f0f0')
        elif float(input) > float(max)/1000 or float(input)< float(min)/1000:
            op5.configure(text='NG',bg='red')
            input6.focus()
            input6.delete(0,'end')
        else:
            op5.configure(text='PASS',bg='green')
            input6.focus()
            input6.delete(0,'end')

ip5.trace_variable('w',checkresult5)
input5=Entry(root,textvariable=ip5,width=10,justify='right')
input5.grid(row=10,column=1,padx=5) 
##input6
ip6 = StringVar()
def checkresult6(var, index, mode):
    input = ip6.get()
    
    if len(input)==5:
        inputs=specinput.get()
        min,max = inputs.split("-")
        input= float(input)
        if input == 0:
            op6.configure(text='',bg='#f0f0f0')
        elif float(input) > float(max)/1000 or float(input)< float(min)/1000:
            op6.configure(text='NG',bg='red')
            input7.focus()
            input7.delete(0,'end')
        else:
            op6.configure(text='PASS',bg='green')
            input7.focus()
            input7.delete(0,'end')
   
Label(root,text='input 6').grid(row=11,column=0,padx=5)
ip6.trace_variable('w',checkresult6)
input6 =Entry(root,textvariable=ip6,width=10,justify='right')
input6.grid(row=11,column=1,padx=5) 
##input7
ip7 = StringVar()
def checkresult7(var, index, mode):
    input = ip7.get()
    print(len(f'{input}'))
    if len(input)==5:
        inputs=specinput.get()
        min,max = inputs.split("-")
        input= float(input)
        if input == 0:
            op7.configure(text='',bg='#f0f0f0')
        elif float(input) > float(max)/1000 or float(input)< float(min)/1000:
            op7.configure(text='NG',bg='red')
            input8.focus()
            input8.delete(0,'end')
        else:
            op7.configure(text='PASS',bg='green')
            input8.focus()
            input8.delete(0,'end')

ip7.trace_variable('w',checkresult7)
Label(root,text='input 7').grid(row=12,column=0,padx=5)
input7 = Entry(root,textvariable=ip7 ,width=10,justify='right')
input7.grid(row=12,column=1,padx=5) 
##input8
ip8 = StringVar()
def checkresult8(var, index, mode):
    input = ip8.get()
    if len(input)==5:
        inputs=specinput.get()
        min,max = inputs.split("-")
        input= float(input)
        if input == 0:
            op8.configure(text='',bg='#f0f0f0')
        elif float(input) > float(max)/1000 or float(input)< float(min)/1000:
            op8.configure(text='NG',bg='red')
            input9.focus()
            input9.delete(0,'end')
        else:
            op8.configure(text='PASS',bg='green')
            input9.focus()
            input9.delete(0,'end')
  
ip8.trace_variable('w',checkresult8)
Label(root,text='input 8').grid(row=13,column=0,padx=5)
input8=Entry(root,textvariable=ip8,width=10,justify='right')
input8.grid(row=13,column=1,padx=5) 
##input9
ip9 = StringVar()
def checkresult9(var, index, mode):
    input = ip9.get()
    if len(input)==5:
        inputs=specinput.get()
        min,max = inputs.split("-")
        input= float(input)
        if input == 0:
            op9.configure(text='',bg='#f0f0f0')
        elif float(input) > float(max)/1000 or float(input)< float(min)/1000:
            op9.configure(text='NG',bg='red')
            input10.focus()
            input10.delete(0,'end')
        else:
            op9.configure(text='PASS',bg='green')
            input10.focus()
            input10.delete(0,'end')


ip9.trace_variable('w',checkresult9)
Label(root,text='input 9').grid(row=14,column=0,padx=5)
input9= Entry(root,textvariable=ip9,width=10,justify='right')
input9.grid(row=14,column=1,padx=5) 
##input10
ip10 = StringVar()
def checkresult10(var, index, mode):
    input = ip10.get()
    if len(input)==5:
        inputs=specinput.get()
        min,max = inputs.split("-")
        input= float(input)
        if input == 0:
            op10.configure(text='',bg='#f0f0f0')
        elif float(input) > float(max)/1000 or float(input)< float(min)/1000:
            op10.configure(text='NG',bg='red')
            input11.focus()
            input11.delete(0,'end')
        else:
            op10.configure(text='PASS',bg='green')
            input11.focus()
            input11.delete(0,'end')
 
ip10.trace_variable('w',checkresult10)
Label(root,text='input 10').grid(row=15,column=0,padx=5)
input10=Entry(root,textvariable=ip10,width=10,justify='right')
input10.grid(row=15,column=1,padx=5)
##input11
ip11 = StringVar()
def checkresult11(var, index, mode):
    input = ip11.get()
    if len(input)==5:
        inputs=specinput.get()
        min,max = inputs.split("-")
        input= float(input)
        if input == 0:
            op11.configure(text='',bg='#f0f0f0')
        elif float(input) > float(max)/1000 or float(input)< float(min)/1000:
            op11.configure(text='NG',bg='red')
            input12.focus()
            input12.delete(0,'end')
        else:
            op11.configure(text='PASS',bg='green')
            input12.focus()
            input12.delete(0,'end')

ip11.trace_variable('w',checkresult11)
Label(root,text='input 11').grid(row=16,column=0,padx=5)
input11=Entry(root,textvariable=ip11,width=10,justify='right')
input11.grid(row=16,column=1,padx=5) 
##input12
ip12 = StringVar()
def checkresult12(var, index, mode):
    input = ip12.get()
    print(input)
    if len(input)==5:
        inputs=specinput.get()
        min,max = inputs.split("-")
        input= float(input)
        if float(input) > float(max)/1000 or float(input)< float(min)/1000:
            op12.configure(text='NG',bg='red')
        else:
            op12.configure(text='PASS',bg='green')

    
ip12.trace_variable('w',checkresult12)
Label(root,text='input 12').grid(row=17,column=0,padx=5)
input12 =Entry(root,textvariable=ip12,width=10,justify='right')
input12.grid(row=17,column=1,padx=5) 


#button Save,Cancle
Button(root, text='Call Data',bg='lime',bd=2,command=on_click).grid(row=18,column=1,pady=5) 
Button(root, text=' reset ',bg='yellow',bd=2,command=cancel).grid(row=18,column=2,pady=5)
#Avg
Label(root, text='Avg',bg='#e0ffff').grid(row=19,column=0,pady=7) 
avg_result=Label(root)
avg_result.grid(row=19,column=1,sticky='news',pady=7)

#cpk
Label(root, text='Cpk',bg='#e0ffff').grid(row=20,column=0,pady=7) 
cpk_result=Label(root)
cpk_result.grid(row=20,column=1,sticky='news',pady=7)
Label(root, text=ym,font=10).grid(row=0,column=3,pady=7) 

#output 
op1=Label(root)
op1.grid(row=6,column=2)
op2=Label(root)
op2.grid(row=7,column=2)
op3=Label(root)
op3.grid(row=8,column=2)
op4=Label(root)
op4.grid(row=9,column=2)
op5=Label(root)
op5.grid(row=10,column=2)
op6=Label(root)
op6.grid(row=11,column=2)
op7=Label(root)
op7.grid(row=12,column=2)
op8=Label(root)
op8.grid(row=13,column=2)
op9=Label(root)
op9.grid(row=14,column=2)
op10=Label(root)
op10.grid(row=15,column=2)
op11=Label(root)
op11.grid(row=16,column=2)
op12=Label(root)
op12.grid(row=17,column=2)
root.mainloop()