import numpy as np
from tkinter import Entry,Frame,Label,Button
from tkinter import E,W,N,S,RIGHT,LEFT,BOTTOM,END

class Operations:
    def __init__(self):
        self.root = None 
        self.maincontent=None 
        self.header = None
        self.Frames = []
        self.boundaries = dict([])
        
    def focusIn(self,widget,placeholder):
        widget.delete(0,END) if widget.get().lower()==placeholder.lower() else False
            
    def focusOut(self,widget,text):
        widget.insert(0,text) if widget.get().lower()=='' or widget.get().lower()==text.lower() else False
        
    def displayOutput(self,Output):
        try:
            
            print("Output",Output)
            if hasattr(self, 'OutputArea') and self.OutputArea.winfo_exists():
                for widget in self.OutputArea.winfo_children():
                    widget.destroy()
            

            for widget in self.OutputArea.winfo_children():
                widget.destroy()
            
            output_label = Label(self.OutputArea,text="Output:",background="green",font=self.matrix_value_font)
            output_label.grid(row=0,column=0,sticky=W)

            if np.ndim(Output) == 0:
                Label(self.OutputArea,text=str(round(float(Output),4)),
                background="green",font=self.matrix_value_font).grid(row=1,column=0,sticky=W)
            else:
                for x,row in enumerate(Output):
                    for y,col in enumerate(row):
                        Label(self.OutputArea,text=f"{col} ",padx=1,pady=1,background="green",font=self.matrix_value_font).grid(row=x+1,column=y+1)
                    
            self.OutputArea.grid(row=6,column=1,sticky="")
        except Exception as e:
            print(e)
            raise 
               
        
    def calculate(self,operation):
        '''This function gets values from the nested entry object loops and'
        stores it to a new list which only contains values. If the fetched value is
        letter, the calculate button will not work.'''
        try:

            gridA=[]
            gridB=[]
            finalA=[]
            finalB=[]
            output = np.array([])
            for row in range(len(self.matrixA)):
                    gridA=[]
                    for col in range(len(self.matrixA[row])):
                        if self.matrixA[row][col].get().isalpha() or self.matrixA[row][col].get()=='' :
                            gridA.append(0.0)
                        else:
                            gridA.append(float(self.matrixA[row][col].get()))
                    finalA.append(gridA)

            if len(self.matrixB)>0:
                
                for row in range(len(self.matrixB)):
                    gridB=[]
                    for col in range(len(self.matrixB[row])):
                        if self.matrixB[row][col].get().isalpha() or self.matrixB[row][col].get()=='':
                            gridB.append(0.0)
                        else:
                            gridB.append(float(self.matrixB[row][col].get()))
                    finalB.append(gridB)
            
            finalA = np.array(finalA)
            finalB = np.array(finalB)

            if operation.lower() == 'addition':
                
                output = np.add(finalA,finalB)
            elif operation.lower() == 'subtraction':
                
                output = np.subtract(finalA, finalB)
            elif operation.lower() == 'multiplication':
                
                output = np.matmul(finalA,finalB)
            elif operation.lower() == 'transpose':
                
                output = np.transpose(finalA)
            elif operation.lower() == 'determinant':
            
                output = np.linalg.det(finalA)

            self.displayOutput(output)
        except Exception as e:
            print(e)
            raise
            
        
    def createElementInputField(self,frame,operation):
        self.matrixA=[]
        self.matrixB=[]

        if hasattr(self, 'Generated') and self.Generated.winfo_exists():
            self.Generated.destroy()
        #This frame is used to contain only generated fields.
        self.Generated = Frame(frame,background="green")
        
        for widget in frame.winfo_children():
            info = widget.grid_info()
            
            if info and int(info['row']) >= 3:
                widget.destroy()
        
        final_row = 0
        total_cols= 0
        two_matrix_ops = ["addition", "subtraction", "multiplication"]
        #A full square is made by r1 * c2
        #This if statement will check if operation requires two matrix, else one matrix.
        
        if operation.lower() in two_matrix_ops:
            r1, c1 = self.boundaries['row1'], self.boundaries['col1'] 
            r2, c2 = self.boundaries['row2'], self.boundaries['col2']

            for r in range(r1):
                row_entry = []
                for c in range(c1):
                    entry = Entry(self.Generated,font=self.matrix_value_font)
                    entry.grid(row=r+3,column=c,padx=1, pady=1)
                    row_entry.append(entry)
                self.matrixA.append(row_entry)

            space = c1+1
            
            for r in range(r2):
                row_entry = []
                for c in range(c2):
                    entry = Entry(self.Generated,font=self.matrix_value_font)
                    entry.grid(row=r+3,column=space+c,padx=1, pady=1)
                    row_entry.append(entry)
                self.matrixB.append(row_entry)
            
            for c in range(c1 + 1 + c2):
                self.Generated.columnconfigure(c, uniform="matrix", weight=1)
            
            final_row = max(r2,r1)+3
            total_cols = c1

        else:
            r, c = self.boundaries['row'], self.boundaries['col']
            
            Label(self.Generated, text="Matrix",font=self.text_font,background="green").grid(row=1, column=0, columnspan=c,sticky="")
            for x in range(r):
                row_entry = []
                for y in range(c):
                    entry = Entry(self.Generated)
                    entry.grid(row=x+3,column=y,padx=1, pady=1)
                    row_entry.append(entry)
                    
                self.matrixA.append(row_entry)

            for c in range(c + 1):
                self.Generated.columnconfigure(c, uniform="matrix", weight=1)

            final_row = r+2 
            total_cols = c

        Button(self.Generated, text="Calculate",
           command=lambda: self.calculate(operation)).grid(
           row=final_row+2, column=0, columnspan=total_cols, pady=5, sticky="")
        
        self.Generated.grid(row=10, column=0, columnspan=6, pady=10, sticky="w")
    def ProcessRowCol(self,operation,frame,**boundaries):
        """
        This function processes the input and checks if row and column input is correct or not.
        """
        data = boundaries['boundaries']
        for key in data:
            if any(char.isalpha() for char in data[key]):
                return
            
            data[key] = 1 if data[key] == '' else int(data[key])

            if data[key] < 1:
                return
                
            self.boundaries[key] = data[key]

        iscorrect = False 

        if operation.lower() == "addition" or operation.lower() == "subtraction":
            iscorrect = (self.boundaries['row1'] == self.boundaries['row2']) and (self.boundaries['col1'] == self.boundaries['col2'])
        elif operation.lower() == "multiplication":
            iscorrect = (self.boundaries['col1'] == self.boundaries['row2'])
        elif operation.lower() == "determinant":
            iscorrect = (self.boundaries['row'] == self.boundaries['col'])
        else:
            iscorrect = (self.boundaries['row']>0 and self.boundaries['col']>0)

        if iscorrect:
            self.dynamic_frame = frame 
            self.createElementInputField(self.dynamic_frame,operation)
        else:
            return
    def setupTwoDimentionInputs(self,frame,operation):
        head_label = Label(frame,text=f"Enter two matrix's max row and column for {operation}",background="green",font=self.text_font)
        head_label.grid(row=0,column=0,columnspan=6,sticky="")
        Label(frame, text="Matrix A", background="green",font=self.text_font).grid(row=1, column=0, columnspan=2,sticky="")
        Label(frame, text="R1:", background="green",font=self.text_font).grid(row=2, column=0, sticky=E)
        row1 = Entry(frame)
        row1.grid(row=2,column=1,sticky=E)

        Label(frame, text="C1:", background="green",font=self.text_font).grid(row=2, column=2, sticky=E)
        col1 = Entry(frame)
        col1.grid(row=2,column=3,sticky=E)

        Label(frame, text="Matrix B", background="green",font=self.text_font).grid(row=1, column=4, columnspan=2,sticky="")
        Label(frame, text="R2:", background="green",font=self.text_font).grid(row=2, column=4, sticky=E)
        row2 = Entry(frame)
        row2.grid(row=2,column=5,sticky=E)

        Label(frame, text="C2:", background="green",font=self.text_font).grid(row=2, column=6, sticky=E)
        col2 = Entry(frame)
        col2.grid(row=2,column=7,sticky=E)

        next_btn = Button(frame,text="Next",width=3,height=1,command=lambda: self.ProcessRowCol(operation,frame,boundaries={"row1":row1.get(),"col1":col1.get(),"row2":row2.get(),"col2":col2.get()}))
        next_btn.grid(row=4,column=0,columnspan=5,pady=5,sticky="")
    
    def setupOneDimentionInput(self,frame,operation):
        head_label = Label(frame,text=f"Enter Matrix's max row and col for {operation}",background="green",font=self.text_font)
        head_label.grid(row=0,column=0,columnspan=2,sticky="")

        row = Entry(frame)
        col = Entry(frame)

        row.grid(row=1,column=0,columnspan=1,sticky=W)
        col.grid(row=1,column=1,columnspan=1,sticky=W)

        next_btn = Button(frame,text="Next",width=3,height=1,command=lambda: self.ProcessRowCol(operation,frame,boundaries={"row":row.get(),"col":col.get()}))
        next_btn.grid(row=2,column=0,columnspan=2,pady=5,sticky="")

        row.insert(0,"Enter max row")
        col.insert(0,"Enter max col")
        row.bind("<FocusIn>",lambda event :self.focusIn(row,"Enter max row"))
        col.bind("<FocusIn>",lambda event :self.focusIn(col,"Enter max column"))
        row.bind("<FocusOut>",lambda event :self.focusOut(row,"Enter max row"))
        col.bind("<FocusOut>",lambda event :self.focusOut(col,"Enter max column"))
        
    def setRoot(self,root,maincontent,header,matrix_value_font,text_font):
        self.root = root 
        self.maincontent=maincontent
        self.header = header
        self.matrix_value_font = matrix_value_font
        self.text_font = text_font

        self.AdditionFrame = Frame(maincontent,background="green",)
        self.SubtractionFrame = Frame(maincontent,background="green")
        self.MultiplicationFrame = Frame(maincontent,background="green")
        self.DeterminantFrame = Frame(maincontent,background="green")
        self.TransposeFrame = Frame(maincontent,background="green")
        self.OutputArea = Frame(maincontent, background="green")
        
        self.Frames = [self.AdditionFrame,
                        self.SubtractionFrame,
                        self.MultiplicationFrame,
                        self.DeterminantFrame,
                        self.TransposeFrame,
                        self.OutputArea]
        
    def clearUI(self):
        for frames in self.Frames:
            frames.grid_remove()  

    def showAdditionComponent(self):       
        self.setupTwoDimentionInputs(self.AdditionFrame,"Addition")
        self.AdditionFrame.grid(row=2, column=1,padx=40,sticky="nw")
        
    def showSubtractionComponent(self):    
        self.setupTwoDimentionInputs(self.SubtractionFrame,"Subtraction")
        self.SubtractionFrame.grid(row=2, column=1,padx=40,sticky="nw")
        
    def showMultiplicationComponent(self):
        self.setupTwoDimentionInputs(self.MultiplicationFrame,"Multiplication")
        self.MultiplicationFrame.grid(row=2, column=1,padx=40,sticky="nw")
        
    def showDeterminantComponent(self):
        self.setupOneDimentionInput(self.DeterminantFrame,"Determinant")
        self.DeterminantFrame.grid(row=2, column=1,padx=40,sticky="nw")
        
    def showTransposeComponent(self):
        self.setupOneDimentionInput(self.TransposeFrame,"Transpose")
        self.TransposeFrame.grid(row=2, column=1,padx=40,sticky="nw")
        
operations = Operations()