import tkinter as tk # Needed for gui
import tkinter.ttk as ttk # Needed for gui
from tkinter import filedialog # Needed to select files
import pyAesCrypt # Needed for aes encryption
import os # Needed for creating files, identifying valid paths, and deleting files
from random import randint # Needed for hacking defense


# Gui created with Pygubu-Designer
class NewprojectApp:

    tempPath = ''
    fileType = ''
    tempExten = ''
    password = [REDACTED]
    invalid = ['!', '@', '#', '$', '%',
                '^', '&', '*', '(', ')',
                '+', '=', '\\', '/', ':'
                ';', '"', "'", '<', '>',
                '?', '|', '{', '}']
    
    def __init__(self, master=None):
        # build ui
        self.MainFrame = tk.Frame(master)
        
        self.encrypt_button = ttk.Button(self.MainFrame)
        self.encrypt_button.config(text='Encrypt a File')
        self.encrypt_button.place(anchor='nw', height='50', relx='0.05', rely='0.25', width='200', x='0', y='0')
        self.encrypt_button.configure(command=self.encrypt)
        
        self.decrypt_button = ttk.Button(self.MainFrame)
        self.decrypt_button.config(text='Decrypt a File')
        self.decrypt_button.place(anchor='nw', height='50', relx='0.05', rely='0.58', width='200', x='0', y='0')
        self.decrypt_button.configure(command=self.decrypt)
        
        self.messageName = ttk.Entry(self.MainFrame)
        _text_ = '''Enter Message Title'''
        self.messageName.delete('0', 'end')
        self.messageName.insert('0', _text_)
        self.messageName.place(anchor='nw', height='25', relx='0.46', rely='.09', width='200', x='0', y='0')
        
        self.Encrypt_Text = ttk.Button(self.MainFrame)
        self.Encrypt_Text.config(text='Encrypt Message')
        self.Encrypt_Text.place(anchor='nw', relx='0.46', rely='0.85', x='0', y='0')
        self.Encrypt_Text.config(command=self.encryptMessage)
        
        self.Secret_Message = tk.Text(self.MainFrame)
        self.Secret_Message.config(height='10', width='50', wrap='word')
        _text_ = '''Enter Message to Encrypt'''
        self.Secret_Message.insert('0.0', _text_)
        self.Secret_Message.place(anchor='nw', height='115', relx='0.46', rely='0.25', width='300', x='0', y='0')

        # To-Do: Make the below feedback text work
        self.feedback = ttk.Label(self.MainFrame)
        self.feedbackText = ''
        self.feedback.config(font='{Arial} 10 {bold}', text=self.feedbackText)
        self.feedback.place(anchor='nw', relx='0.64', rely='0.86', x='0', y='0')
        
        self.separator_1 = ttk.Separator(self.MainFrame)
        self.separator_1.config(orient='vertical', takefocus=False)
        self.separator_1.place(anchor='nw', height='200', relx='0.43', rely='0.0', width='3', x='0', y='0')
        
        self.label_mess = ttk.Label(self.MainFrame)
        self.label_mess.config(text='Create Encrypted\n       Message')
        self.label_mess.place(anchor='nw', relx='0.81', rely='0.07', x='0', y='0')
                               
        self.label_file = ttk.Label(self.MainFrame)
        self.label_file.config(text='Encrypt or Decrypt Individual Files')
        self.label_file.place(anchor='nw', relx='0.06', rely='.09', x='0', y='0')
                               
        self.MainFrame.config(height='200', takefocus=False, width='600')
        self.MainFrame.pack(side='top')
        
        # Main widget
        self.mainwindow = self.MainFrame

    def encrypt(self): # This function will encrypt files
        try:
            self.tempExten = ''
            pathway = filedialog.askopenfilename(initialdir='', title='Select a File to Encrypt', filetypes=(("All Files", "*.*"), ('Text', '*.txt')))
            self.tempPath = pathway
            self.getPathExt()

            if self.tempExten == '.aes': #Something here causes an error that aborts the operation. This is accidental success, as I want it to fail in this case.
                self.Secret_Messge.insert('0.0', 'Please Select a Non-Encrypted File')
                self.Secret_Message.place()
            
            fileName = self.getName(path=pathway, encrypt=True)
            
            
            if pathway != '' and pathway != 'No File Selected':
                bit = 64 * 1024
                pyAesCrypt.encryptFile(pathway, fileName + self.tempExten + '.aes', self.password, bit)

            else:
                pass

        except:
            pass

    def decrypt(self): # This function will decrypt files
        try:
            # 1. Clear extension variable, get path
            self.tempExten = ''
            pathway = filedialog.askopenfilename(initialdir='', title='Select a File to Encrypt', filetypes=(("Encrypted Files", "*.aes"), ('Invalid Files', '*.*')))
            self.tempPath = pathway

            # 2. Identify pre-encryption filetype
            self.getOldExt()

            # 3. Identify the name of the file
            fileName = self.getName(path=pathway, encrypt=False)

            # 4. Begin decryption process
            if pathway != '' and pathway != 'No File Selected':
                bit = 64 * 1024
                pyAesCrypt.decryptFile(pathway, fileName + self.tempExten, self.password, bit)

            else:
                pass

        except:
            pass

    def getName(self, path, encrypt): # This function will determine the name of files

        name = [] # Empty list predefined for appending
        periodCt = 0 # This variable will hold the number of encountered periods
        pos = -1 # This will be our index as we iterate backwards
        trigger = 0 # This tells us when to stop iterating through the path

        # 1. Determine if the operation is decryption or encryption, set appropriate trigger
        if encrypt == True:
            trigger = 1

        else:
            trigger = 2
            
        # 2. Iterate backwards until period threshold has been met
        while periodCt < trigger:
            if path[pos] != '.':
                pos -= 1

            else:
                periodCt += 1
                pos -= 1
                if not periodCt < trigger:
                    break

        # 3. Append every char encountered until a forward slash is detected
        while path[pos] != '/':
            name.append(path[pos])
            pos -= 1

        # 4. Correct the list's orientation, then compile into single string
        name.reverse()
        fullName = ''
        fullName = fullName.join(name)

        # 5. Send out the name
        return fullName


    def getPathExt(self): # This function will determine the extension of unencrypted files 
        position = -1 # Index as we iterate backwards
        extension = [] # Empty list for appending

        # 1. Append the list until a period has been encountered
        while True:
            if self.tempPath[position] != '.':
                extension.append(self.tempPath[position])
                position -= 1
            else:
                extension.append('.')
                break

        # 2. Correct list orientation, then compile into string
        extension.reverse()        
        self.tempExten = self.tempExten.join(extension)


    def getOldExt(self): # This function will get the old extension of encrypted files 
        position = -1 # This will be our index as we iterate backwards
        extension = [] # Empty list predefined for appending
        perCt = 0 # This tells us how many periods we've encountered

        # 1. Iterate backwards until a period has been passed, then append
        #    the list until the second period is encountered (format = .old.aes)
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

        # 2. Correct list orientation, then assign the extentsion string to tempExten
        extension.reverse()
        self.tempExten = self.tempExten.join(extension)
    

    def encryptMessage(self): # This function will encrypt a new message

        #1. Get message contents, determine if name is valid (if not, clean it)
        toEncode = self.Secret_Message.get("1.0", "end-1c")
        subject = self.messageName.get()

        # 1.5 Clean invalid names
        
        for item in self.invalid: # Look at every invalid symbol
            for char in subject: # Look at every character in the name
                if item in char: # If an invalid symbol is found at the character position
                    subject = subject.replace(char, '') # Replace it with an empty character
                    
        
        #2. Save message to file

        # Hacking vulnerability: using the same name would allow an adversary to stalk folder until it appears
        # and intercept the message before it gets encrypted and deleted.
        #
        # Solution: randomize the file names and extensions

        # 2.1 create random file name of length 16
        randFileName = self.getRandName(size=16)
        
        # 2.2 create random file extension of length 4
        randExten = '.' + self.getRandName(size=4)
        
        
        oldFile = open(randFileName + randExten, 'w')
        oldFile.write(toEncode)
        oldFile.close()

        #3. Encrypt message and save to aes file
        bit = 64 * 1024
        pyAesCrypt.encryptFile(randFileName + randExten, subject + '.txt.aes', self.password, bit)
    
        #4. Corrupt original file's data
        oldFile = open(randFileName + randExten, 'w')
        corrupt = open('seed.ksf', 'r')

        uselessData = corrupt.read() # Stores the useless data on random 
        oldFile.write(uselessData) # Writes the useless data on random to the file, hopefully replacing any traces of the original message
        oldFile.close()
        corrupt.close()

        
        #5. Delete original file
        if os.path.exists(randFileName + randExten) == True:
            os.remove(randFileName + randExten)
            #success = open('success.txt', 'w')
            #success.write('Fuck that old file. It\'s gone now! Name = ' + randFileName + randExten)
            #success.close()

        else:
            pass

    def getRandName(self, size):
        randName = []
        numOrChar = randint(0, 1)
        
        for char in range(size):
            if numOrChar == 0: # Use Number
                randName.append(chr(randint(48, 57)))

            else: # Use Character
                randName.append(chr(randint(97, 122)))

            numOrChar = randint(0, 1) # Reset the chance


        newName = ''
        newName = newName.join(randName)

        return newName
        
    def run(self):
        self.mainwindow.mainloop()

if __name__ == '__main__':
    import tkinter as tk
    root = tk.Tk()
    root.resizable(height=False, width=False) #Prohibit resizing the height or width of window
    root.wm_title("EnKryptos v0.2.0.1") # Sets the title of the window to the string included as an argument
    
    app = NewprojectApp(root)
    app.run()

