from tkinter import *

class my_Buttonbox(object):
    def __init__(self,parent):

        self.master = Toplevel(parent)
        lableframe=Frame(self.master )
        lableframe.grid(row=0, column=0)
        Bframe=Frame(self.master )
        Bframe.grid(row=1, column=0)
        self.label=Label(lableframe, text="Choose the correct label? (if you close this window, Nothing will be saved)")
        self.label.pack(pady=20,padx=10)
        self.b0 = Button(Bframe, text="Basophil",height=2, width=15,command=self.e0)
        self.b0.grid(row=0, column=0)
        self.b1 = Button(Bframe, text="Lymphoblast",height=2, width=15,command=self.e1)
        self.b1.grid(row=0, column=1,padx=10)
        self.b2 = Button(Bframe, text="Myeloblast",height=2, width=15,command=self.e2)
        self.b2.grid(row=0, column=2,padx=10)
        self.b3 = Button(Bframe, text="Monoblast",height=2, width=15,command=self.e3)
        self.b3.grid(row=0, column=3,padx=10)
        self.b4 = Button(Bframe, text="Promonocyte",height=2, width=15,command=self.e4)
        self.b4.grid(row=1, column=0)
        self.b5 = Button(Bframe, text="Prolymphocyte",height=2, width=15,command=self.e5)
        self.b5.grid(row=1, column=1,padx=10)
        self.b6 = Button(Bframe, text="Hypo promyelocytes",height=2, width=15,command=self.e6)
        self.b6.grid(row=1, column=2,padx=10)
        self.b7 = Button(Bframe, text="Hyper promyelocytes",height=2, width=15,command=self.e7)
        self.b7.grid(row=1, column=3,padx=10)
        self.b8 = Button(Bframe, text="Myelocytes",height=2, width=15,command=self.e8)
        self.b8.grid(row=2, column=0)
        self.b9 = Button(Bframe, text="Hairy Cell",height=2, width=15,command=self.e9)
        self.b9.grid(row=2, column=1,padx=10)
        self.b10 = Button(Bframe, text="Meta",height=2, width=15,command=self.e10)
        self.b10.grid(row=2, column=2,padx=10)
        self.b11 = Button(Bframe, text="Band",height=2, width=15,command=self.e11)
        self.b11.grid(row=2, column=3,padx=10)
        self.b12 = Button(Bframe, text="Baso Normoblast",height=2, width=15,command=self.e12)
        self.b12.grid(row=3, column=0)
        self.b13 = Button(Bframe, text="Poly Normoblast",height=2, width=15,command=self.e13)
        self.b13.grid(row=3, column=1,padx=10)
        self.b14 = Button(Bframe, text="Ortho Normoblast ",height=2, width=15,command=self.e14)
        self.b14.grid(row=3, column=2,padx=10)
        self.b15 = Button(Bframe, text="Other",height=2, width=15,command=self.e15)
        self.b15.grid(row=3, column=3,padx=10)
        self.master.deiconify()
        self.master.wait_window()
        #self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        #self.master.mainloop()
    def e0(self):
        self.label=0
        self.master.destroy()
    def e1(self):
        self.label=1
        self.master.destroy()
    def e2(self):
        self.label=2
        self.master.destroy()
    def e3(self):
        self.label=3
        self.master.destroy()

    def e4(self):
        self.label = 4
        self.master.destroy()

    def e5(self):
        self.label = 5
        self.master.destroy()

    def e6(self):
        self.label = 6
        self.master.destroy()

    def e7(self):
        self.label = 7
        self.master.destroy()

    def e8(self):
        self.label = 8
        self.master.destroy()

    def e9(self):
        self.label = 9
        self.master.destroy()

    def e10(self):
        self.label = 10
        self.master.destroy()

    def e11(self):
        self.label = 11
        self.master.destroy()

    def e12(self):
        self.label = 12
        self.master.destroy()

    def e13(self):
        self.label = 13
        self.master.destroy()

    def e14(self):
        self.label = 14
        self.master.destroy()

    def e15(self):
        self.label = 15
        self.master.destroy()

    #def on_closing(self):
        #self.label=None
        #self.master.destroy()
