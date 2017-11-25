
# Modules needed for GUI Implementation
# -------------------------------------
# Importing wx files
import wx
# Importing wordwrap for formatting text in AboutDialog
from wx.lib.wordwrap import wordwrap
# For system-specific functions
import sys
import pdb

# Modules needed for Semaphore Implementation
# -------------------------------------------
from threading import Thread, Lock
import thread
import threading
import time
import random

# Global variables
# ----------------
Slices = 8
numStudents = 5
SliceCount=8

# Semaphore variable declarations for Semaphore Implementation
# ------------------------------------------------------------
sem_emptybox = threading.Semaphore(0)
sem_fullbox = threading.Semaphore(0)
sem_print = threading.Semaphore(1)
sem_Slices = threading.Semaphore(1)

# Classes and other variable declarations for GUI Implementation
# --------------------------------------------------------------
class MainPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, pos=(0,0), size=(669,240))
        self.SetBackgroundStyle(wx.BG_STYLE_ERASE)
        self.frame = parent

        vSizer = wx.BoxSizer(wx.VERTICAL)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)

        AboutBtn = wx.Button(self, id=wx.ID_ANY, label="About")
    	AboutBtn.Bind(wx.EVT_BUTTON, self.AboutDialog)
    	vSizer.Add(AboutBtn, 0, wx.ALL, 5)

    	StartBtn = wx.Button(self, id=wx.ID_ANY, label="Start")
    	StartBtn.Bind(wx.EVT_BUTTON, self.StartSimulation)
    	vSizer.Add(StartBtn, 0, wx.ALL, 5)

        # Turn this into a help button
    	ExitBtn = wx.Button(self, id=wx.ID_ANY, label="Exit")
    	ExitBtn.Bind(wx.EVT_BUTTON, self.ExitWindow)
    	vSizer.Add(ExitBtn, 0, wx.ALL, 5)

    	hSizer.Add((1,1), 1, wx.EXPAND)
        hSizer.Add(vSizer, 0, wx.TOP, 10)
        hSizer.Add((1,1), 0, wx.ALL, 10)
        self.SetSizer(hSizer)

    	self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

    def AboutDialog(self, evt):
    	info = wx.AboutDialogInfo()
    	info.name = "Pizzaphiles!"
    	info.Version = "0.0.1 Beta"
    	info.Description = wordwrap("This is an application that simulates the solution of the Pizza Eating Problem with semaphores using wxPython!", 350, wx.ClientDC(self))
        info.WebSite = ("https://docs.google.com/document/d/1r2ypHw_ca-hdEnm0XNoshhmdQN6UY1ENbKJQQ3uxYWs/edit#heading=h.8aqpxrfsx4k1", "The Problem Statement")
        info.Developers = ["Jeffrey Jacob (CED15I036)", "Mukundhan Kumar (CED15I005)", "Aditya Prakash (CED15I025)"]
        wx.AboutBox(info)

    def StartSimulation(self, event):
        self.frame.StartSimulating()

    def ExitWindow(self, event):
        sys.exit()

    def OnEraseBackground(self, event):
        # Add a picture to the background
        dc = event.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = wx.Bitmap("studentroom.gif")
        dc.DrawBitmap(bmp, 0, 0)


class MainFrame(wx.Frame):
    # studentIcon = None
    StudentIconList = [ ]
    pizzaIconList = [ ]

    def __init__(self):
        """Constructor"""
        # pdb.set_trace()
        FrameStyle = wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER | wx.RESIZE_BOX | wx.MAXIMIZE_BOX)
        wx.Frame.__init__(self, None, size=(669,341), title="Pizzaphiles!", style=FrameStyle)
        panel1 = MainPanel(self)

        for i in xrange(0,numStudents):
            self.studentIcon = wx.StaticBitmap(panel1, wx.ID_ANY, wx.Bitmap('Scott Pilgrim.png', wx.BITMAP_TYPE_ANY), pos=wx.Point(90*i,40))
            # self.studentIcon.Hide()
            self.studentIcon.Show()            
            self.StudentIconList.append(self.studentIcon)
    
        for i in xrange(0,Slices):
            self.pizzaIcon = wx.StaticBitmap(panel1, wx.ID_ANY, wx.Bitmap('8bit-pizza.png', wx.BITMAP_TYPE_ANY), pos=wx.Point(70*i,120))
            # self.pizzaIcon.Hide()
            self.pizzaIcon.Show()
            self.pizzaIconList.append(self.pizzaIcon)

        self.deliveryguyIcon = wx.StaticBitmap(panel1, wx.ID_ANY, wx.Bitmap('deliveryguy8bit.png', wx.BITMAP_TYPE_ANY), pos=wx.Point(480,170))
        # self.deliveryguyIcon.Hide()
        self.deliveryguyIcon.Show()

        # print self.StudentIconList
        # self.ShowImage()


        # self.statusbar = self.CreateStatusBar(1)
        # self.statusbar.SetStatusText("Loading...")
        self.SetIcon(wx.Icon("pizza16x16.png"))     
        self.Center()
        self.Show()

    def StartSimulating(self):
        stud_id = [ ]
        students_thread = [ ]
        
        for i in xrange(numStudents+1):
            stud_id.append(0)
        
        thread_list = []
        for i in xrange(numStudents):
            stud_id[i]=i
            students_thread=threading.Thread(target = self.student, args = (stud_id[i],))
            thread_list.append(students_thread)
            # students_thread.start()

        print thread_list

        for i in xrange(len(thread_list)):
            thread_list[i].start()
            
        # students_thread=threading.Thread(target = self.deliveryguy, args = (stud_id[i+1],))
        # students_thread.start()

        # self.studentIcon.Show()

        for i in xrange(numStudents): 
            students_thread.join()
        return None

    def student(self, student_id):
        global SliceCount
        x=0
        while (x<3):
            sem_Slices.acquire()
            if (SliceCount==0):
                sem_emptybox.release()
                print "\nStudent %d called the delivery boy" %(student_id+1)
                sem_fullbox.acquire()
                SliceCount = 8
            SliceCount = SliceCount-1
            x = x+1
            # pdb.set_trace()
            sem_print.acquire()


            self.StudentIconList[student_id].Show()
            print "Student %d is eating" %(student_id+1)
            sem_print.release()
            time.sleep(2)
            print "No. of slices left: %d" %(SliceCount)
            self.StudentIconList[student_id].Hide()
            sem_Slices.release()

            time.sleep(2)

            sem_print.acquire()
            print "\nStudent %d is done eating" %(student_id+1)
            sem_print.release()
        thread.exit()

    def deliveryguy(self,deliveryguy_id):
        x=0
        while (x<3):
            time.sleep(2)
            sem_emptybox.acquire()
            self.deliveryguyIcon.Show()
            print "\nDelivery guy filled the box\n"
            time.sleep(2)
            self.deliveryguyIcon.Hide()            
            sem_fullbox.release()
            x = x+1
        thread.exit()

    def ShowImage(self):
        for i in xrange(numStudents):
            self.StudentIconList[i].Show()

class Main(wx.App):
    def __init__(self, redirect=False, filename="None"):
        """Constructor"""
        wx.App.__init__(self, redirect, filename)
        MainFrame()

# Main program: starts up the app
# -------------------------------
if __name__ == "__main__":
    app = Main()
    app.MainLoop()