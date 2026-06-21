from tkinter import Tk,Label,Frame, Radiobutton,StringVar,font
from Operations import operations

class MatrixOperationsTool():
    def __init__(self,root):
        self.framePlacementPos=0
        self.selected = None 
        self.matrix_value_font = font.Font(family="Courier",size=15)
        self.text_font = font.Font(family="Arial",size=11,weight="bold")
        self.root = root
        self.root.config(background="gray")
        self.root.title("Matrix Operations tool")
        self.root.geometry("950x400")
        
        self.header = Frame(root,background="gray",height=50)
        self.header.pack(padx=20,side="top")
        
        self.maincontent = Frame(root,background="green")
        self.maincontent.pack(side="bottom",fill="both",expand=True)
        
        self.selectionFrame = Frame(self.maincontent,background="green")
    def UIOption(self):
        '''
        This function checks what i clicked using self.selected
        '''
        option = self.selected.get()
        operations.clearUI()

        if option.lower() == "addition":
            operations.showAdditionComponent()
            
        elif option.lower() == "subtraction":
            operations.showSubtractionComponent()
            
        elif option.lower() == "multiplication":
            operations.showMultiplicationComponent()

        elif option.lower() == "transpose":
            operations.showTransposeComponent()

        elif option.lower() == "determinant":
            operations.showDeterminantComponent()

        else:
            return 
        return None 
    
    def setupHeader(self):
        input_label = Label(self.header,text="Input",background="gray",font=self.text_font)
        output_label = Label(self.header,text="Output",background="gray",font=self.text_font)

        input_label.pack(side="left",padx="100")        
        output_label.pack(side="right",padx="100")

    def setupBody(self):
        """
        This function sets up layers of UI. 
        eg: User will click through if he / she wants to add, subtract, multiply, etc..
        If its a transpose, only for one matrix this UI will ask. If its something else, 
        There will be two matrix inputs
        """

        label_pos=0
        self.framePlacementPos=0
        currentframepos=self.framePlacementPos
        
        self.selectionFrame = Frame(self.maincontent,background="green")
        
        heading_1 = Label(self.selectionFrame,text="What operation you would like to perform?",background="green",font=self.text_font)
        heading_1.grid(row=label_pos+1,column=label_pos+3,padx=5)

        selected = StringVar(value="Addition of matrix")
        self.selected = selected

        addition_option = Radiobutton(self.selectionFrame,text="Addition of matrix", variable=selected, value="Addition",command=self.UIOption,background="green") 
        addition_option.grid(row=label_pos+2,column=label_pos+3,pady=2)

        subtraction_option = Radiobutton(self.selectionFrame,text="Subtraction of matrix", variable=selected, value="Subtraction",command=self.UIOption,background="green")
        subtraction_option.grid(row=label_pos+3,column=label_pos+3,pady=2)
        
        multiplication_option = Radiobutton(self.selectionFrame,text="Multiplication of matrix", variable=selected, value="Multiplication",command=self.UIOption,background="green")
        multiplication_option.grid(row=label_pos+4,column=label_pos+3,pady=2)
        
        transpose_option = Radiobutton(self.selectionFrame,text="Transpose of matrix", variable=selected, value="Transpose",command=self.UIOption,background="green")
        transpose_option.grid(row=label_pos+5,column=label_pos+3,pady=2)
        
        determinant_option =Radiobutton(self.selectionFrame,text="Determinant of matrix", variable=selected, value="Determinant",command=self.UIOption,background="green")
        determinant_option.grid(row=label_pos+6,column=label_pos+3,pady=2)

        self.selectionFrame.grid(row=currentframepos,column=0,padx=4, sticky="nw")
        self.maincontent.columnconfigure(0,weight=0)
        self.maincontent.columnconfigure(1,weight=1)
        self.maincontent.columnconfigure(2,weight=0)

if __name__ == "__main__":
    root = Tk()
    matrixtool = MatrixOperationsTool(root)
    operations.setRoot(root,matrixtool.maincontent,matrixtool.header,matrixtool.matrix_value_font,matrixtool.text_font,matrixtool.framePlacementPos)
    matrixtool.setupHeader()
    matrixtool.setupBody()
    root.mainloop()



