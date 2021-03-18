import tkinter as tk
import tkinter.ttk as ttk
from PIL import ImageTk, Image
from tkinter import filedialog # Used to select files
import pyAesCrypt # Used for AES encryption

class NewprojectApp:

    tempPath = ''
    fileType = ''
    tempExten = ''
    password = [REDACTED] # The password has been stricken from the sourcecode. 
    
    def __init__(self, master=None):
        # build ui
        self.MainFrame = tk.Frame(master)
        self.encrypt_button = tk.Button(self.MainFrame)
        self.encrypt_button.config(text='Encrypt')
        self.encrypt_button.place(anchor='nw', height='50', relx='0.07', rely='0.13', width='200', x='0', y='0')
        self.encrypt_button.configure(command=self.encrypt)
        self.decrypt_button = tk.Button(self.MainFrame)
        self.decrypt_button.config(text='Decrypt')
        self.decrypt_button.place(anchor='nw', height='50', relx='0.07', rely='0.58', width='200', x='0', y='0')
        self.decrypt_button.configure(command=self.decrypt)
        self.MainFrame.config(height='200', takefocus=False, width='233')
        self.MainFrame.pack(side='top')

        # Main widget
        self.mainwindow = self.MainFrame

    def encrypt(self):
        try:
            print('encrypt!')
            self.tempExten = ''
            pathway = filedialog.askopenfilename(initialdir='', title='Select a File to Encrypt', filetypes=(("All Files", "*.*"), ('Text', '*.txt')))
            self.tempPath = pathway
            print('Path1 = ' + pathway)
            print('Path2 = ' + self.tempPath)
            self.getPathExt()
            
            if pathway != '' and pathway != 'No File Selected':
                buffer = 64 * 1024
                pyAesCrypt.encryptFile(pathway, 'EncryptedFile' + self.tempExten + '.aes', self.password, buffer)

            else:
                print('Error: No Pathway Detected')

        except:
            print('Operation Aborted')

    def decrypt(self):
        try:
            print('decrypt!')
            self.tempExten = ''
            pathway = filedialog.askopenfilename(initialdir='', title='Select a File to Encrypt', filetypes=(("Encrypted Files", "*.aes"), ('Invalid Files', '*.*')))
            self.tempPath = pathway
            
            print('Path1 = ' + pathway)
            print('Path2 = ' + self.tempPath)
            self.getOldExt()
            
            if pathway != '' and pathway != 'No File Selected':
                buffer = 64 * 1024
                pyAesCrypt.decryptFile(pathway, 'decryptedFile' + self.tempExten, self.password, buffer)

            else:
                print('Error: No Pathway Detected')

        except:
            print('Operation Aborted')

    def getPathExt(self):
        position = -1
        extension = []
        
        while True:
            if self.tempPath[position] != '.':
                extension.append(self.tempPath[position])
                position -= 1
            else:
                extension.append('.')
                break

        extension.reverse()        
        self.tempExten = self.tempExten.join(extension)
        print('Extension = ' + self.tempExten)


    def getOldExt(self):
        position = -1
        extension = []
        perCt = 0

        while True:
            if self.tempPath[position] != '.' and perCt == 0:
                position -= 1

            elif self.tempPath[position] == '.' and perCt == 0:
                perCt = 1
                position -= 1

            elif self.tempPath[position] != '.' and perCt == 1:
                extension.append(self.tempPath[position])
                position -= 1

            elif self.tempPath[position] == '.' and perCt == 1:
                extension.append('.')
                break

            else:
                position -= 1

        extension.reverse()
        print(str(extension))
        self.tempExten = self.tempExten.join(extension)
        print('Old Extension = ' + self.tempExten)
    
    
    def run(self):
        self.mainwindow.mainloop()

if __name__ == '__main__':
    import tkinter as tk
    root = tk.Tk()
    root.resizable(height=False, width=False) #Prohibit resizing the height or width of window
    root.wm_title("EnKryptos") # Sets the title of the window to the string included as an argument
    
    app = NewprojectApp(root)
    app.run()

