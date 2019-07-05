import tkinter
import PIL.Image, PIL.ImageTk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import numpy as np
import os
from B_box import my_Buttonbox

def compute_resize_factor(h,w,win_h,win_w):
  print(h)
  print(win_h)
  rf=(0.85*win_h)/h
  while True:
    rf -= 0.01
    if rf*w<(0.95*win_w):
        print(rf)
        return rf
    rf-=0.01


# The factory function
def dnd_start(source, event):
    h = DndHandler(source, event)
    if h.root:
        return h
    else:
        return None


# The class that does the work

class DndHandler:

    root = None

    def __init__(self, source, event):
        if event.num > 5:
            return
        root = event.widget._root()
        try:
            root.__dnd
            return # Don't start recursive dnd
        except AttributeError:
            root.__dnd = self
            self.root = root
        self.source = source
        self.target = None
        self.initial_button = button = event.num
        self.initial_widget = widget = event.widget
        self.release_pattern = "<B%d-ButtonRelease-%d>" % (button, button)
        self.save_cursor = widget['cursor'] or ""
        widget.bind(self.release_pattern, self.on_release)
        widget.bind("<Motion>", self.on_motion)
        widget['cursor'] = "hand2"

    def __del__(self):
        root = self.root
        self.root = None
        if root:
            try:
                del root.__dnd

            except AttributeError:
                pass

    def on_motion(self, event):
        x, y = event.x_root, event.y_root
        target_widget = self.initial_widget.winfo_containing(x, y)
        source = self.source
        new_target = None
        while target_widget:
            try:
                attr = target_widget.dnd_accept
            except AttributeError:
                pass
            else:
                new_target = attr(source, event)
                if new_target:
                    break
            target_widget = target_widget.master
        old_target = self.target
        if old_target is new_target:
            if old_target:
                old_target.dnd_motion(source, event)
        else:
            if old_target:
                self.target = None
                old_target.dnd_leave(source, event)
            if new_target:
                new_target.dnd_enter(source, event)
                self.target = new_target

    def on_release(self, event):
        self.finish(event, 1)

    def cancel(self, event=None):
        self.finish(event, 0)

    def finish(self, event, commit=0):
        target = self.target
        source = self.source
        widget = self.initial_widget
        root = self.root
        try:
            del root.__dnd
            self.initial_widget.unbind(self.release_pattern)
            self.initial_widget.unbind("<Motion>")
            widget['cursor'] = self.save_cursor
            self.target = self.source = self.initial_widget = self.root = None
            if target:
                if commit:
                    target.dnd_commit(source, event)
                else:
                    target.dnd_leave(source, event)
        finally:
            source.dnd_end(target, event)



# ----------------------------------------------------------------------
# The rest is here for testing and demonstration purposes only!

class Icon:

    def __init__(self, name,type=-1,prev=False):
        self.name = name
        self.canvas = self.label = self.id = None
        self.prev=prev
        self.type=type

    def attach(self, canvas, x=100, y=100,w_s=100):

        if canvas is self.canvas:
            self.canvas.coords(self.id, x, y)
            return
        if self.canvas:
            self.detach()
        if not canvas:
            return
        txt=self.name
        ww=5
        hh=1
        ccolor='red'
        if self.prev:
            txt='type '+self.type
            ww=5
            hh=2
            ccolor='blue'
        label = tkinter.Label(canvas, text=txt,
                              borderwidth=0,bg=ccolor,cursor="hand1",height=hh, width=ww)

        id = canvas.create_window(x, y-w_s, window=label, anchor="nw")
        self.canvas = canvas
        self.label = label
        self.id = id
        label.bind("<ButtonPress>", self.press)


    def detach(self):
        canvas = self.canvas
        if not canvas:
            return
        id = self.id
        label = self.label
        self.canvas = self.label = self.id = None
        canvas.delete(id)
        label.destroy()

    def press(self, event):
        if dnd_start(self, event):
            # where the pointer is relative to the label widget:
            self.x_off = event.x
            self.y_off = event.y
            # where the widget is relative to the canvas:
            self.x_orig, self.y_orig = self.canvas.coords(self.id)

    def putback(self):
        self.canvas.coords(self.id, self.x_orig, self.y_orig)

    def where(self, canvas, event,w_s=100):
        # where the corner of the canvas is relative to the screen:
        x_org = canvas.winfo_rootx()
        y_org = canvas.winfo_rooty()
        # where the pointer is relative to the canvas widget:
        x = event.x_root - x_org
        y = event.y_root - y_org
        cell_x=x
        cell_y=y+w_s
        # compensate for initial pointer offset
        return x - self.x_off, y - self.y_off,cell_x,cell_y

    def dnd_end(self, target, event):
        pass
class App1:
 def __init__(self, window, window_title):
     self.window = window
     self.window.title(window_title)
     self.widthpixels = self.window.winfo_screenwidth()
     self.heightpixels = self.window.winfo_screenheight()
     print(self.heightpixels,  self.widthpixels)
     self.resize_factor = None
     self.window.geometry('{}x{}'.format(self.widthpixels, self.heightpixels))
     self.button_frame = Frame(self.window)
     self.button_frame.pack(side=BOTTOM, fill=Y)
     self.button_frame2 = Frame(self.window)
     self.button_frame2.pack(side=LEFT, fill=Y)
     self.img_frame = Frame(self.window)
     self.img_frame.pack(anchor=tkinter.CENTER, expand=True)
     labelframe1 = LabelFrame(self.button_frame, text='')
     labelframe1.pack(fill="both", expand="yes")
     self.labelframe3 = LabelFrame(self.window, text='')
     self.labelframe3.pack(side=BOTTOM, fill=Y)
     labelframe2 = LabelFrame(self.button_frame2, text='Working panel')
     labelframe2.pack(fill="both", expand="yes")
     self.choose_button = Button(labelframe2, text='import folder', height=2, width=10, command=self.select)
     self.choose_button.grid(row=0, column=0)
     self.start_button = Button(labelframe2, text='start', height=2, width=10, command=self.start)
     self.start_button.grid(row=1, column=0)
     self.start_button.config(state="disabled")
     self.prev_button = Button(labelframe1, text='Prev', height=1, width=10,command=self.prev)
     self.prev_button.grid(row=0, column=1)
     self.prev_button.config(state="disabled")
     self.next_button = Button(labelframe1, text='Next', height=1, width=10,command=self.next)
     self.next_button.grid(row=0, column=2)
     self.next_button.config(state="disabled")
     self.cancel_button = Button(labelframe2, text='cancel', height=2, width=10,command=self.cancel)
     self.cancel_button.grid(row=3, column=0)
     self.cancel_button.config(state="disabled")
     self.addt_button = Button(labelframe2, text='Add cell', height=2, width=10,cursor="plus",command=self.add_tracker)
     self.addt_button.grid(row=2, column=0)
     self.addt_button.config(state="disabled")
     temp = ttk.Separator(labelframe2, orient=HORIZONTAL)
     temp.grid(row=4, column=0, pady=10, sticky="ew")
     self.wsize_label=Label(labelframe2,text='Window Size: 100')
     self.wsize_label.grid(row=5, column=0,pady=10)
     size_frame=Frame(labelframe2)
     size_frame.grid(row=6, column=0)
     self.up_size = Button(size_frame, text='+', height=2, width=5,command=self.up_size)
     self.up_size.grid(row=0, column=0)
     self.down_size = Button(size_frame, text='-', height=2, width=5,command=self.down_size)
     self.down_size.grid(row=0, column=1)
     self.var = IntVar()
     self.def_size=Checkbutton(labelframe2, text="set as default size",variable=self.var,command=self.change_size)
     self.def_size.grid(row=7, column=0)
     temp2 = ttk.Separator(labelframe2, orient=HORIZONTAL)
     temp2.grid(row=8, column=0, pady=10, sticky="ew")
     self.video_selected=False
     self.tracker_num=0
     self.Icons=[]
     self.add_selected=False
     self.vid=None
     if os.path.exists('window_size.txt'):
         with open('window_size.txt', "r")  as ins2:
             lines = ins2.read().splitlines()
             self.p_size=int(lines[0])
             ss = 'Window Size: ' + str(self.p_size)
             self.wsize_label.config(text=ss)

     else:
        self.p_size=100
     self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

 def close_help(self):
     self.helpmaster.destroy()
 def change_size(self):
     #print(self.var.get())
     if self.var.get():
         ff=open('window_size.txt','w')
         ff.write(str(self.p_size)+'\n')
         ff.close()
 def up_size(self):
     self.p_size+=5
     ss='Window Size: '+str(self.p_size)
     self.wsize_label.config(text=ss)
     print(self.tracker_num)
     self.load_all()



 def down_size(self):
     self.p_size-=5
     ss='Window Size: '+str(self.p_size)
     self.wsize_label.config(text=ss)
     print(self.tracker_num)
     self.load_all()


 def get_frame(self,frame_number):
     if frame_number>=0 and frame_number<self.frame_num:
         #frame=cv2.imread(self.frames[frame_number])
         #img=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
         img = PIL.Image.open(self.frames[frame_number])
         double_size = (int(img.size[0] * self.resize_factor), int(img.size[1] * self.resize_factor))
         img1 = np.asanyarray(img.resize(double_size))
         #img1=cv2.resize(img,(0,0),fx=self.resize_factor,fy=self.resize_factor)
         return (img1,True)
     else:
         return (None,False)
 def add_tracker(self):
     self.window.config(cursor='plus')
     self.add_selected = True
 def add_tracker2(self,xx,yy):
     self.tracker_num+=1
     k=self.tracker_num-1
     tracker_name=str(self.tracker_num)
     self.Icons.append(Icon(tracker_name))
     self.Icons[k].attach(self.canvas,xx,yy,self.p_size)
     self.Icons[k].label.bind("<Button-3>", lambda event, a=k: self.right_click(event,a))
     self.canvas.create_rectangle(xx-self.p_size,yy-self.p_size,xx+self.p_size,yy+self.p_size)
     self.canvas.create_oval(xx-1,yy-1,xx+1,yy+1)
     self.cell_mid.append([xx,yy])
     self.rect_xy.append([xx-self.p_size,yy-self.p_size,xx+self.p_size,yy+self.p_size])
     ff=open(self.out_folder + '/'+tracker_name+'.txt', 'w')
     ff.write(str(int(xx/self.resize_factor)) + ',' + str(int(yy/self.resize_factor)) + '\n')
     ff.close()

 def right_click(self,event,k):
     self.menu = Menu(self.canvas, tearoff=0)
     self.menu.add_radiobutton(label='label and save',command=lambda a=k: self.tag(k))
     self.is_right=True
     self.menu.post(event.x_root, event.y_root)
 def load_all(self):
     for child in self.canvas.winfo_children():
         child.destroy()
     img, ret = self.get_frame(self.frame_counter)
     ww = np.size(img,0)
     hh = np.size(img,1)
     print(hh,ww)
     self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(img))
     self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
     self.tracker_num = 0
     self.Icons = []
     self.rect_xy = []
     self.cell_mid = []
     self.add_selected = False
     self.is_right = False
     self.out_folder = self.video_folder + '/' + self.frame_names[self.frame_counter]
     if os.path.exists(self.out_folder) == False:
         os.makedirs(self.out_folder)
     else:

         names=[]
         for root, dirnames, filenames in os.walk(self.out_folder):
             for filename in filenames:
                 if filename.endswith(".txt"):
                     names.append(int(filename.split('.')[0]))
         if len(names)>0:
             self.tracker_num =max(names)
             for k in range(0,self.tracker_num):
                 tracker_name = str(k+1)
                 ff = open(self.out_folder+'/'+tracker_name+'.txt', 'r')
                 aa = ff.readline()
                 xx = int(aa.split(',')[0])*self.resize_factor
                 yy = int(aa.split(',')[1])*self.resize_factor
                 self.Icons.append(Icon(tracker_name))
                 self.Icons[k].attach(self.canvas, xx, yy, self.p_size)
                 self.Icons[k].label.bind("<Button-3>", lambda event, a=k: self.right_click(event, a))
                 self.canvas.create_rectangle(xx - self.p_size, yy - self.p_size, xx + self.p_size,
                                              yy + self.p_size)
                 self.canvas.create_oval(xx - 1, yy - 1, xx + 1, yy + 1)
                 self.cell_mid.append([xx, yy])
                 self.rect_xy.append([xx - self.p_size, yy - self.p_size, xx + self.p_size, yy + self.p_size])















 def start(self):

     self.start_button.config(state="disabled")
     self.choose_button.config(state="disabled")
     for child in self.img_frame.winfo_children():
         child.destroy()
     self.tracker_num=0
     self.Icons=[]
     self.rect_xy=[]
     self.cell_mid=[]
     self.add_selected = False
     self.is_right=False
     #self.window_size=100
     self.next_button.config(state="normal")
     self.prev_button.config(state="normal")
     self.cancel_button.config(state="normal")
     self.addt_button.config(state="normal")
     self.prev_label=0
     if os.path.exists('output') == False:
         os.makedirs('output')
     out_name = self.video_source.split('/')[-1]
     if os.path.exists('output/' + out_name) == False:
         os.makedirs('output/' + out_name)
     matches = []
     names=[]
     for root, dirnames, filenames in os.walk(self.video_source):
         for filename in filenames:
             if filename.endswith(".jpg"):
                 matches.append(os.path.join(root, filename))
                 names.append(filename)
     self.frames=matches
     self.frame_names=names
     self.frame_num=len(matches)
     self.video_folder='output/' + out_name
     #img=cv2.imread(matches[0])
     img =np.asanyarray( PIL.Image.open(matches[0]))
     self.width=np.size(img,1)
     self.height=np.size(img,0)
     self.resize_factor = compute_resize_factor(self.height, self.width, self.heightpixels, self.widthpixels)
     #img,ret=self.get_frame(0)
     #ww = np.size(img,0)
     #hh = np.size(img,1)
     #print(hh,ww)
     #print(self.height, self.width)
     #print(int(self.height * self.resize_factor),int(self.width * self.resize_factor))
     self.canvas = tkinter.Canvas(self.img_frame, width=int(self.width*self.resize_factor), height=int(self.height*self.resize_factor))
     self.canvas.pack()
     self.canvas.bind('<Button-1>', self.click)
     self.canvas.dnd_accept = self.dnd_accept
     self.frame_counter = -1
     self.next()



 def click_bar(self,event,k):
     print('click:'+str(k))
 def click(self,event):
     if self.add_selected:
         self.add_selected=False
         self.window.config(cursor='arrow')
         self.add_tracker2(event.x,event.y)
     if self.is_right:
         self.menu.destroy()
         self.is_right = False
         self.resume()


 def select(self):
     for child in self.img_frame.winfo_children():
         child.destroy()
     #self.filename = filedialog.askopenfilename(initialdir="/home", title="Select a file",
     #                                           filetypes=(("Video files", "*.mp4"), ("all files", "*.*")))
     dirr = os.getcwd()
     self.filename = filedialog.askdirectory(initialdir=dirr,
                                             title="Select a folder",
                                             )
     if self.filename!=None:

         self.start_button.config(state="normal")
         self.video_source = self.filename



 def next(self):
     self.frame_counter+=1
     if self.frame_counter==self.frame_num:
         self.frame_counter=0
     img,ret=self.get_frame(self.frame_counter)
     if ret:
         self.load_all()
     else:
         self.frame_counter -= 1

 def prev(self):
     self.frame_counter-=1
     img,ret=self.get_frame(self.frame_counter)
     if ret:
         self.load_all()
     else:
         self.frame_counter += 1







 def tag(self,cell_num):
     #choosed= eg.buttonbox("Choose the correct label? (if you close this window, Nothing will be saved)",
     #                            choices=["Healthy", "First type", "Second type","Unknown"])
     ch=my_Buttonbox(self.window)
     choosed=ch.label
     k=cell_num
     if type(choosed)==int:
         label=int(choosed)
         ff = open(self.out_folder + '/' + str(k+1) + '.txt', 'r')
         aa=ff.readline()
         ff.close()
         ff = open(self.out_folder + '/' + str(k+1) + '.txt', 'w')
         ff.write(aa+str(label)+'\n')
         ff.write(str(self.p_size) + '\n')
         ff.close()




 def cancel(self):
     for child in self.img_frame.winfo_children():
         child.destroy()
     for child in self.labelframe3.winfo_children():
         child.destroy()
     self.prev_button.config(state="disabled")
     self.next_button.config(state="disabled")
     self.cancel_button.config(state="disabled")
     self.addt_button.config(state="disabled")
     self.start_button.config(state="normal")
     self.choose_button.config(state="normal")





 def on_closing(self):

     self.window.destroy()


 def dnd_accept(self, source, event):
     return self
 def dnd_enter(self, source, event):
     k=self.name_dict[source.name]
     if k>=0:
        self.rect_xy[k]=None
     self.canvas.focus_set() # Show highlight border
     x, y,mx,my = source.where(self.canvas, event,self.p_size)
     if k>=0:
         self.cell_mid[k][0]=mx
         self.cell_mid[k][1]=my

     x1, y1, x2, y2 = source.canvas.bbox(source.id)
     dx, dy = x2-x1, y2-y1
     self.dndid = self.canvas.create_rectangle(x, y, x+dx, y+dy)
     self.dnd_motion(source, event)

 def dnd_motion(self, source, event):
     k=self.name_dict[source.name]
     x, y,mx,my = source.where(self.canvas, event,self.p_size)
     if k>=0:
         self.cell_mid[k][0]=mx
         self.cell_mid[k][1]=my
         self.rect_xy[k] =[self.cell_mid[k][0]-self.p_size,self.cell_mid[k][1]-self.p_size,self.cell_mid[k][0]+self.p_size,self.cell_mid[k][1]+self.p_size]
     x1, y1, x2, y2 = self.canvas.bbox(self.dndid)
     self.canvas.move(self.dndid, x-x1, y-y1)

 def dnd_leave(self, source, event):
     self.window.focus_set() # Hide highlight border
     self.canvas.delete(self.dndid)
     self.dndid = None

 def dnd_commit(self, source, event):
     k = self.name_dict[source.name]
     self.dnd_leave(source, event)
     x, y,mx,my  = source.where(self.canvas, event,self.p_size)
     if k>=0:
         self.cell_mid[k][0]=mx
         self.cell_mid[k][1]=my
     source.attach(self.canvas, x, y)


a=App1(tkinter.Tk(),'Nimaad labeling App')
a.window.mainloop()
