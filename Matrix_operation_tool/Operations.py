import numpy as np
from tkinter import Entry,Frame,Label,Button,TclError
from tkinter import W,END

class Operations:
    def __init__(self):
        self.root=None 
        self.maincontent=None 
        self.header=None
        self.Frames=[]
        self.boundaries=dict([])
        self.selectedFrame=None
        self.InputFrame=None

    def focusIn(self,widget,placeholder):
        widget.delete(0,END) if widget.get().lower()==placeholder.lower() else False
            
    def focusOut(self,widget,text):
        widget.insert(0,text) if widget.get().lower()=='' or widget.get().lower()==text.lower() else False
        
    def displayOutput(self,Output):
        try:
            y=0
            element_pos=0
            self.framePlacementPos=0
            currentframepos=self.framePlacementPos
            if hasattr(self, 'OutputArea') and self.OutputArea.winfo_exists():
                for widget in self.OutputArea.winfo_children():
                    widget.destroy()
            
            for widget in self.OutputArea.winfo_children():
                widget.destroy()
            
            output_label = Label(self.OutputArea,text="Output",background="green",font=self.matrix_value_font)
            output_label.grid(row=element_pos+2,column=0)

            if np.ndim(Output)==0:
                Label(self.OutputArea,text=str(round(float(Output),4)),
                background="green",font=self.matrix_value_font).grid(row=element_pos+3,column=0,sticky='nw')
            else:
                for x,row in enumerate(Output):
                    for y,col in enumerate(row):
                        Label(self.OutputArea,text=f"{col} ",padx=1,pady=1,background="green",font=self.matrix_value_font).grid(row=x+element_pos+3,column=y+1,sticky='nw')
            
            output_label.grid(columnspan=y)
            self.OutputArea.grid(row=currentframepos+1,column=1,sticky="nw")
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
            
        
    def createElementInputField(self,operation):
        try:
            self.framePlacementPos=0
            currentframepos=self.framePlacementPos

            self.matrixA=[]
            self.matrixB=[]

            if not self.InputFrame:
                return 
            
            if hasattr(self,'InputFrame') and self.InputFrame.winfo_children():
                for widget in self.InputFrame.winfo_children():
                    widget.destroy()
            
            total_cols=0
            new_block_pos=0
            r=0
            if operation.lower() in ["addition", "subtraction", "multiplication"]:
                r1, c1 = self.boundaries['row1'], self.boundaries['col1'] 
                r2, c2 = self.boundaries['row2'], self.boundaries['col2']

                Label(self.InputFrame, text="Matrix A", font=self.text_font, background="green").grid(row=0, column=1, columnspan=c1, pady=(0,5), sticky="w")
                
                for r in range(r1):
                    row_entry=[]
                    for c in range(c1):
                        if r1>3:
                            entry=Entry(self.InputFrame,font=self.matrix_value_font,width=2)
                            entry.grid(row=r+1,column=c,sticky="w")
                        else:
                            entry=Entry(self.InputFrame,font=self.matrix_value_font)
                            entry.grid(row=r+1,column=c,padx=1, pady=1,sticky="w")
                        row_entry.append(entry)
                    self.matrixA.append(row_entry)

                new_block_pos=r1+2
                Label(self.InputFrame, text="Matrix B", font=self.text_font, background="green").grid(row=new_block_pos, column=1, columnspan=c2, pady=(0,5), sticky="w")                
                for r in range(r2):
                    row_entry=[]
                    for c in range(c2):
                        if r2>3:
                            entry=Entry(self.InputFrame,font=self.matrix_value_font,width=2)
                            entry.grid(row=r+new_block_pos+1,column=c,sticky="w")
                        else:
                            entry=Entry(self.InputFrame,font=self.matrix_value_font)
                            entry.grid(row=r+new_block_pos+1,column=c,padx=1, pady=1,sticky="w")
                        
                        row_entry.append(entry)
                    self.matrixB.append(row_entry)
                
                total_cols = c1 + c2

            else:
                r,c = self.boundaries['row'], self.boundaries['col']
                
                Label(self.InputFrame, text="Matrix",font=self.text_font,background="green").grid(row=new_block_pos+r, column=0, columnspan=c, sticky="w")
                for x in range(r):
                    row_entry=[]
                    for y in range(c):
                        if x>3:
                            entry=Entry(self.InputFrame,font=self.matrix_value_font,width=2)
                            entry.grid(row=x+1,column=y,sticky="w")
                        else:
                            entry=Entry(self.InputFrame,font=self.matrix_value_font)
                            entry.grid(row=x+1,column=y,padx=1, pady=1,sticky="w")
                        row_entry.append(entry)
                        
                    self.matrixA.append(row_entry)

                for c in range(c+2):
                    self.InputFrame.columnconfigure(c, uniform="matrix", weight=1)

                total_cols = c

            Button(self.InputFrame, text="Calculate",
            command=lambda: self.calculate(operation)).grid(
            row=new_block_pos+r+2, column=0, columnspan=total_cols, pady=5, sticky="")
            
            self.InputFrame.grid(row=currentframepos, column=1, pady=10, sticky="nw")
        
        except TclError as e:
            print(e)
            raise
        except Exception as e:
            print(e)
            raise
    def ProcessRowCol(self,operation,**boundaries):
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
            self.createElementInputField(operation)
        else:
            return
        
    def setupTwoDimentionInputs(self,frame,operation):
        self.selectedFrame = frame
        label_pos=0
        head_label = Label(self.selectedFrame,text=f"Enter two matrix's max row and column for {operation}",background="green",font=self.text_font)
        head_label.grid(row=label_pos+1,column=0,columnspan=6,sticky="")

        Label(self.selectedFrame,text="Matrix A",background="green",font=self.text_font).grid(row=label_pos+2,column=0,columnspan=2,sticky="")
        Label(self.selectedFrame,text="R1:",background="green",font=self.text_font).grid(row=label_pos+3,column=0,sticky="e")
        row1=Entry(self.selectedFrame)
        row1.grid(row=label_pos+3,column=1, padx=2, pady=2)

        Label(self.selectedFrame,text="C1:",background="green",font=self.text_font).grid(row=label_pos+4, column=0, sticky="e")
        col1=Entry(self.selectedFrame)
        col1.grid(row=label_pos+4,column=1, padx=2, pady=2)

        Label(self.selectedFrame, text="Matrix B",background="green",font=self.text_font).grid(row=label_pos+2, column=4, columnspan=2,sticky="")
        Label(self.selectedFrame, text="R2:",background="green",font=self.text_font).grid(row=label_pos+3, column=4, sticky="e")
        row2=Entry(self.selectedFrame)
        row2.grid(row=label_pos+3,column=5, padx=2, pady=2)

        Label(self.selectedFrame,text="C2:",background="green",font=self.text_font).grid(row=label_pos+4, column=4, sticky="e")
        col2=Entry(self.selectedFrame)
        col2.grid(row=label_pos+4,column=5, padx=2, pady=2)

        next_btn=Button(self.selectedFrame,text="Next",width=6,height=1,command=lambda: self.ProcessRowCol(operation,boundaries={"row1":row1.get(),"col1":col1.get(),"row2":row2.get(),"col2":col2.get()}))
        next_btn.grid(row=label_pos+5,column=0,columnspan=6,pady=10,sticky="")
    
    def setupOneDimentionInput(self,frame,operation):
        self.selectedFrame = frame
        label_pos=0
        head_label=Label(self.selectedFrame,text=f"Enter Matrix's max row and col for {operation}",background="green",font=self.text_font)
        head_label.grid(row=label_pos+1,column=0,columnspan=2,sticky="")

        Label(self.selectedFrame,text="Rows:", background="green",font=self.text_font).grid(row=label_pos+2, column=0, sticky="e")
        row=Entry(self.selectedFrame)
        row.grid(row=label_pos+2,column=1, padx=2, pady=2)

        Label(self.selectedFrame, text="Columns:", background="green",font=self.text_font).grid(row=label_pos+3, column=0, sticky="e")
        col=Entry(self.selectedFrame)
        col.grid(row=label_pos+3,column=1, padx=2, pady=2)

        next_btn=Button(self.selectedFrame,text="Next",width=6,height=1,command=lambda: self.ProcessRowCol(operation,boundaries={"row":row.get(),"col":col.get()}))
        next_btn.grid(row=label_pos+4,column=0,columnspan=2,pady=10,sticky="")

        row.insert(0,"Enter max row")
        col.insert(0,"Enter max col")
        row.bind("<FocusIn>",lambda event :self.focusIn(row,"Enter max row"))
        col.bind("<FocusIn>",lambda event :self.focusIn(col,"Enter max col"))
        row.bind("<FocusOut>",lambda event :self.focusOut(row,"Enter max row"))
        col.bind("<FocusOut>",lambda event :self.focusOut(col,"Enter max col"))
        
    def setRoot(self,root,maincontent,header,matrix_value_font,text_font,framePlacementPos):
        '''
        This function sets essentials for Operations.py from Main python file
        '''
        self.framePlacementPos = framePlacementPos
        self.root = root 
        self.maincontent = maincontent
        self.header = header
        self.matrix_value_font = matrix_value_font
        self.text_font = text_font
        
        self.AdditionFrame=Frame(self.maincontent,background="green")
        self.SubtractionFrame=Frame(self.maincontent,background="green")
        self.MultiplicationFrame=Frame(self.maincontent,background="green")
        self.DeterminantFrame=Frame(self.maincontent,background="green")
        self.TransposeFrame=Frame(self.maincontent,background="green")
        self.OutputArea=Frame(self.maincontent, background="green")
        self.InputFrame=Frame(self.maincontent, background="green")

        self.Frames = [self.AdditionFrame,
                       self.SubtractionFrame,
                       self.MultiplicationFrame,
                       self.DeterminantFrame,
                       self.TransposeFrame,
                       self.InputFrame,
                        self.OutputArea]
        
    def clearUI(self):
        for frames in self.Frames:
            frames.grid_remove()  

    def showAdditionComponent(self):       
        self.setupTwoDimentionInputs(self.AdditionFrame,"Addition")
        self.AdditionFrame.grid(row=self.framePlacementPos+3, column=0, padx=10, pady=10, sticky="nw")
        
    def showSubtractionComponent(self):    
        self.setupTwoDimentionInputs(self.SubtractionFrame,"Subtraction")
        self.SubtractionFrame.grid(row=self.framePlacementPos+3, column=0, padx=10, pady=10, sticky="nw")
        
    def showMultiplicationComponent(self):
        self.setupTwoDimentionInputs(self.MultiplicationFrame,"Multiplication")
        self.MultiplicationFrame.grid(row=self.framePlacementPos+3, column=0, padx=10, pady=10, sticky="nw")
        
    def showDeterminantComponent(self):
        self.setupOneDimentionInput(self.DeterminantFrame,"Determinant")
        self.DeterminantFrame.grid(row=self.framePlacementPos+3, column=0, padx=10, pady=10, sticky="nw")
        
    def showTransposeComponent(self):
        self.setupOneDimentionInput(self.TransposeFrame,"Transpose")
        self.TransposeFrame.grid(row=self.framePlacementPos+3, column=0, padx=10, pady=10, sticky="nw")
        
operations = Operations()