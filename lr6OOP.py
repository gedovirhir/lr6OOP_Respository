import clr
import random
import time
from abc import ABC, abstractmethod
import numpy as np

clr.AddReference('System')
clr.AddReference('System.IO')
clr.AddReference('System.Drawing')
clr.AddReference('System.Reflection')
clr.AddReference('System.Threading')
clr.AddReference('System.Windows.Forms')

from System import EventHandler
import System.IO
import System.Drawing as Dr
import System.Reflection
import System.Windows.Forms as WinForm

class __storageList__(ABC): #снаружи наше "хранилище" ведет себя как список
    @abstractmethod
    def __init__(self): #ининциализация списка
        pass
    def add(self, x, index): #добавление элемента по индексу
        pass
    def getNode(self, index): #получение узла по индексу
        pass
    def cotnains(self, name): #проверка наличия элемента в узлах списка
        pass
    def isEmpty(self): #проверяет список на наличие хотя бы 1го элемента 
        pass
    def deleteIndex(self, index): #удаление элемента по индексу
        pass
    def deleteNode(self, node): 
        pass
    def clear(self): #очистка списка
        pass 


class Node(object):
    def __init__(self, x = None, v = None):
        self.key = x
        self.next = None
        self.prev = v
    
    def deleteThis(self):
        if self.prev:
            self.prev.next = self.next
        if self.next:
            self.next.prev = self.prev
        del self

class storage(__storageList__):
    def __init__(self):
        self.head = None
        self.len = 0
    
    def add(self, x, index = None):
        newNode = Node(x)
        if self.head is None:
            self.head = newNode
            self.len += 1
            return
        lastNode = self.head
        if index:
            for i in range(index):
                if (lastNode.next):
                    lastNode = lastNode.next
        else:
            while lastNode.next:
                lastNode = lastNode.next
        if lastNode.next:
            lastNode.next.prev = newNode
            newNode.next = lastNode.next
        lastNode.next = newNode
        newNode.prev = lastNode
        self.len += 1
    
    def getNode(self, index):
        if index > self.len-1: IndexError("IndexError")
        lastNode = self.head
        for i in range(index):
            lastNode = lastNode.next
        return lastNode
    
    def cotnains(self, name):
        lastNode = self.head
        while (lastNode):
            if name == lastNode.key:
                return True
            else:
                lastNode = lastNode.next
        return False

    def isEmpty(self):
        if self.head:
            return False
        else:
            return True

    def deleteIndex(self, index):
        lastNode = self.head
        if index == 0:
            self.head = lastNode.next
            if lastNode.next:
                lastNode.next.prev = None
            self.len -= 1
            return
        lastNode = self.getNode(index)
        
        lastNode.deleteThis()

        del lastNode
        self.len -= 1

    def deleteNode(self, node):
        if node is self.head:
            self.head = node.next
            node.deleteThis()
            self.len -= 1
            return
        node.deleteThis()
        self.len -= 1

    def clear(self):
        for i in range(self.len):
            self.deleteIndex(0)

class ObjectStorage(storage):
    def __init__(self):
        super().__init__()
        self.handler = EventHandler
        self.objectsList = [CCircle, square, triangle, line]   
        self.lastPressedNode = None   
    def add(self, x, index = None):
        super().add(x,index)
        self.handler.Invoke(self, None)

    def select(self, node, CtrlPressed):
        if CtrlPressed:
            node.key.selected = True
        else:
            forwardNode = node.next
            prevNode = node.prev
            node.key.selected = True
            while forwardNode:
                forwardNode.key.selected = False
                forwardNode = forwardNode.next
            while prevNode:
                prevNode.key.selected = False
                prevNode = prevNode.prev
        self.handler.Invoke(self, None)
    def iterationOfSelectedWithFunc(self, func, *args):
        someNode = self.head
        for i in range(self.len):
            if someNode.key.selected:
                func(someNode, *args)
            someNode = someNode.next
    def deleteSelected(self):
        self.iterationOfSelectedWithFunc(self.deleteNode)
        
        self.handler.Invoke(self, None)
    def drawNodeObject(self, node, flagGraphics, drawPen):
        drawPen.Color = node.key.color
        node.key.draw(flagGraphics, drawPen)
    def drawAllObjects(self, flagGraphics, drawPen):
        for i in range(self.len):
            self.drawNodeObject(self.getNode(i), flagGraphics, drawPen)
    def hitNodeInfo(self, node, X, Y):
        return(node.key.checkBorder(X,Y))
    def hitInfo(self, X, Y):
        for i in range(self.len):
            if self.hitNodeInfo(self.getNode(i), X, Y):
                return self.getNode(i)
        return None
    def changeSizeNode(self, node, val):
        node.key.changeSize(val)
        self.handler.Invoke(self, None)
    def changeSizeSelected(self, val):
        self.iterationOfSelectedWithFunc(self.changeSizeNode, val)
    def changeCordsNode(self, node, deltaX, deltaY):
        node.key.changeCords(deltaX,deltaY)
        self.handler.Invoke(self, None)
    def changeCordsSelected(self, deltaX,deltaY):
        self.iterationOfSelectedWithFunc(self.changeCordsNode,deltaX, deltaY)
    def changeColorNode(self, node, color):
        node.key.color = color
        self.handler.Invoke(self,None)
    def changeColorSelected(self, color):
        self.iterationOfSelectedWithFunc(self.changeColorNode, color)
    
    
    
class figure(object):
    def __init__(self, x, y, color):
        self.xcord = x
        self.ycord = y
        self.color = color

        self.selected = False
    def checkBorder(self, X, Y):
        return(self.xcord == X) and (self.ycord == Y)
    def changeCords(self, deltaX,deltaY):
        self.xcord += deltaX
        self.ycord += deltaY
class CCircle(figure):
    def __init__(self, x, y,color):
        super().__init__(x,y,color)

        self.rad = 15
    def draw(self, flagGraphics, drawPen):
        if self.selected:
            flagGraphics.FillEllipse(Dr.Brushes.LightGreen, self.xcord - self.rad, self.ycord-self.rad, self.rad*2,self.rad*2)
        flagGraphics.DrawEllipse(drawPen,self.xcord - self.rad, self.ycord-self.rad, self.rad*2,self.rad*2)
    def checkBorder(self, X, Y):
        return ((self.xcord + self.rad)>X>(self.xcord - self.rad)) and ((self.ycord + self.rad)>Y>(self.ycord - self.rad))
    def changeSize(self, val):
        self.rad = 15 + val
    def __str__(self):
        return "Circle"
    
    
class square(figure):
    def __init__(self, x, y, color):
        super().__init__(x,y,color)

        self.width = 30
        self.height = 30
    def draw(self, flagGraphics, drawPen):
        if self.selected:
            flagGraphics.FillRectangle(Dr.Brushes.LightGreen, self.xcord, self.ycord, self.width,self.height)
        flagGraphics.DrawRectangle(drawPen,self.xcord, self.ycord, self.width,self.height)
    def checkBorder(self, X,Y):
        return ((self.xcord) < X < (self.xcord + self.width)) and ((self.ycord)<Y<(self.ycord + self.height))
    def changeSize(self, val):
        self.width = 30 + val
        self.height = 30 + val
    def __str__(self):
        return "Square"
    
class triangle(figure):
    def __init__(self, x, y,color):
        super().__init__(x,y,color)

        self.width = 30
        self.height = int(round(self.width*(np.sin(np.deg2rad(60)))))
        self.updatePoints()
    def updatePoints(self):
        self.points = [Dr.Point(self.xcord,self.ycord), Dr.Point(self.xcord+self.width,self.ycord), Dr.Point(self.xcord+(self.width//2), self.ycord+self.height)]
    
    def draw(self, flagGraphics, drawPen):
        self.updatePoints()
        if self.selected:
            flagGraphics.FillPolygon(Dr.Brushes.LightGreen, self.points)
        flagGraphics.DrawPolygon(drawPen,self.points)
    def checkBorder(self, X, Y):
        return ((self.xcord)<X<(self.xcord + self.width)) and ((self.ycord)<Y<(self.ycord+(X-self.xcord)*np.sqrt(3)))
    def changeSize(self, val):
        self.width = 30 + val
        self.height = int(round(self.width*(np.sin(np.deg2rad(60)))))
    def __str__(self):
        return "Triangle"
        
class line(figure):
    def __init__(self, x,y,color):
        super().__init__(x,y,color)
        self.lengh = 100
        self.x1 = self.xcord+self.lengh
        self.y1 = self.ycord
    def draw(self, flagGraphics, drawPen):
        bruh = Dr.Pen(Dr.Brushes.LightGreen)
        bruh.Width = 3
        if self.selected:
            flagGraphics.DrawLine(bruh,self.xcord, self.ycord, self.x1, self.y1)
            return
        flagGraphics.DrawLine(drawPen,self.xcord, self.ycord, self.x1, self.y1)
    def checkBorder(self, X, Y):
        return self.ycord+15 > Y > self.ycord-15
    def changeSize(self, val):
        self.lengh = 100 + val
        self.x1 = self.xcord+self.lengh
    def __str__(self):
        return "Line"




class form1(System.Windows.Forms.Form):
    def __init__(self):        
        self.Text = "form"
        self.BackColor = Dr.Color.FromArgb(238,238,238)
        self.ClientSize = Dr.Size(1800,900)
        caption_height = WinForm.SystemInformation.CaptionHeight
        self.MinimumSize =Dr.Size(392,(117 + caption_height))
        self.KeyPreview  = True

        self.CtrlPressed = False
        self.leftBPressed = None

        self.canvas = Dr.Bitmap(1, 1)
        self.flagGraphics = Dr.Graphics.FromImage(self.canvas)
        self.ObjectStorage = ObjectStorage()

        self.drawPen = Dr.Pen(Dr.Brushes.DeepSkyBlue)
        self.drawPen.Width = 2
        
        self.InitiliazeComponent()
        
    
    def run(self):
        WinForm.Application.Run(self)
    
    def InitiliazeComponent(self):
        self.components = System.ComponentModel.Container()
        self.ImagePB = WinForm.PictureBox()
        self.butt = WinForm.Button()
        self.SwitchObjCB = WinForm.ComboBox()
        self.ChangeSizeSB = WinForm.HScrollBar()
        self.SizeLabel = WinForm.Label()
        self.SwitchColorCB = WinForm.ComboBox()
        self.SwitchColorB = WinForm.Button()

        self.ObjectStorage.handler = EventHandler(self.drawObjects)

        self.KeyDown += self.Form_KeyDown
        self.KeyUp += self.Form_KeyUp
        #self.MouseDown += self.Form_MouseDown
        #self.MouseUp += self.Form_MouseUp

        self.ImagePB.Location = Dr.Point(10, 10)
        self.ImagePB.Size = Dr.Size(1200, 700)
        self.ImagePB.TabStop = False
        self.ImagePB.BorderStyle = WinForm.BorderStyle.Fixed3D
        self.ImagePB.MouseDown += self.ImagePB_KeyDown
        self.ImagePB.MouseUp += self.ImagePB_MouseUp

        self.butt.Location = Dr.Point(1250+60,420)
        self.butt.Size = Dr.Size(200, 50)
        self.butt.BackColor = Dr.Color.FromArgb(238,238,240)
        self.butt.Text = "Очистить"
        self.butt.UseVisualStyleBackColor = 0
        self.butt.FlatStyle = WinForm.FlatStyle.Flat
        self.butt.FlatAppearance.BorderSize = 0
        self.butt.Click += self.butt_Click

        self.SwitchObjCB.Location = Dr.Point(1250,10)
        self.SwitchObjCB.Size = Dr.Size(300,300)
        self.SwitchObjCB.Sorted = False
        self.SwitchObjCB.Items.AddRange([ "Circle","Square", "Triangle", "Line" ])
        self.SwitchObjCB.SelectedIndex = 2
        self.SwitchObjCB.DropDownStyle = WinForm.ComboBoxStyle.DropDownList

        self.SwitchColorCB.Location = Dr.Point(1250,220)
        self.SwitchColorCB.Size = Dr.Size(300,300)
        self.SwitchColorCB.Sorted = False
        self.SwitchColorCB.Items.AddRange([ "Black", "Aqua", "DeepSkyBlue", "Brown", "Coral", "HotPink"])
        self.SwitchColorCB.SelectedIndex = 2
        self.SwitchColorCB.DropDownStyle = WinForm.ComboBoxStyle.DropDownList
        
        self.SwitchColorB.Location = Dr.Point(1250+60,250)
        self.SwitchColorB.Size = Dr.Size(200, 50)
        self.SwitchColorB.BackColor = Dr.Color.FromArgb(238,238,240)
        self.SwitchColorB.Text = "Сменить цвет"
        self.SwitchColorB.UseVisualStyleBackColor = 0
        self.SwitchColorB.FlatStyle = WinForm.FlatStyle.Flat
        self.SwitchColorB.FlatAppearance.BorderSize = 0
        self.SwitchColorB.Click += self.SwitchColorB_Click
        
        self.ChangeSizeSB.Location = Dr.Point(1250,50)
        self.ChangeSizeSB.Size = Dr.Size(300,20)
        self.ChangeSizeSB.ValueChanged += self.ChangeSizeSB_ValueChanged

        self.SizeLabel.Location = Dr.Point(1250+120,90)
        self.SizeLabel.Size = Dr.Size(200,20)
        self.SizeLabel.Text = "Size Change"       
        
        
        self.Controls.Add(self.ImagePB)
        self.Controls.Add(self.butt)
        self.Controls.Add(self.SwitchObjCB)
        self.Controls.Add(self.ChangeSizeSB)
        self.Controls.Add(self.SizeLabel)
        self.Controls.Add(self.SwitchColorCB)
        self.Controls.Add(self.SwitchColorB)
    def dispose(self):
        self.components.Dispose()
        WinForm.Form.Dispose(self)

    def drawObjects(self, sender, args):
        self.ImagePB.Image = None
        self.canvas = Dr.Bitmap(self.ImagePB.Width, self.ImagePB.Height)
        self.flagGraphics = Dr.Graphics.FromImage(self.canvas)

        self.ObjectStorage.drawAllObjects(self.flagGraphics, self.drawPen)

        self.ImagePB.Image = self.canvas

    def Form_KeyDown(self, sender, args):
        if args.KeyCode == WinForm.Keys.ControlKey:
            self.CtrlPressed = True
        if args.KeyCode == WinForm.Keys.Delete:
            self.ObjectStorage.deleteSelected()
    def Form_KeyUp(self, sender, args):
        if args.KeyCode == WinForm.Keys.ControlKey:
            self.CtrlPressed = False
    def ImagePB_MouseUp(self, sender, args):
        if args.Button == WinForm.MouseButtons.Left and self.ObjectStorage.lastPressedNode:
            deltaX = args.X - self.ObjectStorage.lastPressedNode.key.xcord
            deltaY = args.Y - self.ObjectStorage.lastPressedNode.key.ycord
            if (abs(deltaX) > 10 or abs(deltaY) > 10):
                self.ObjectStorage.changeCordsSelected(deltaX, deltaY)
            self.ObjectStorage.lastPressedNode = None

    def ImagePB_KeyDown(self, sender, args):
        if args.Button == WinForm.MouseButtons.Right:
            self.ObjectStorage.add(self.ObjectStorage.objectsList[self.SwitchObjCB.SelectedIndex](args.X, args.Y, self.drawPen.Color))

        elif args.Button == WinForm.MouseButtons.Left:
            self.leftBPressed = True
            if self.ObjectStorage.hitInfo(args.X, args.Y):
                self.ObjectStorage.select((self.ObjectStorage.hitInfo(args.X, args.Y)), self.CtrlPressed)
                self.ObjectStorage.lastPressedNode = self.ObjectStorage.hitInfo(args.X, args.Y)

    def ChangeSizeSB_ValueChanged(self, sender, args):
        self.ObjectStorage.changeSizeSelected(self.ChangeSizeSB.Value)
    
    def SwitchColorB_Click(self, sender, args):
        self.drawPen.Color = Dr.Color.FromName(self.SwitchColorCB.SelectedItem)
        self.ObjectStorage.changeColorSelected(self.drawPen.Color)

                    

        
    def butt_Click(self, sender, args):
        self.ImagePB.Image = None
        self.flagGraphics = Dr.Graphics.FromImage(self.canvas)
        self.ObjectStorage.clear()
        self.canvas = Dr.Bitmap(self.ImagePB.Width, self.ImagePB.Height)




def form_thr():
    form = form1()

    WinForm.Application.Run(form)
    form.dispose()


if __name__ == '__main__':
    form_thr()
