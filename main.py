# Gui created with Pygubu-Designer
import tkinter.ttk as ttk  # Needed for gui
from tkinter import filedialog  # Needed to select files
import pyAesCrypt  # Needed for aes encryption and decryption of files
import pyAesCryptMod as messageMod  # Needed for message encryption (allows me to use pseudo-files)
import os  # Needed for creating files, identifying valid paths, and deleting files
from random import randint  # Needed for key generation
from io import StringIO as fakeFile  # Needed for hacking defense (prevents hard-drive files from being created)
import threading  # Allows EnKryptos to run smoother by preventing it from freezing with large files / arduous tasks


class EnKryptosGUI:
    workLock = False  # This prevents more operations from being performed simultaneously
    homeDir = os.getcwd()  # Will hold pathway to EnKryptos' working directory
    opSys = os.name  # If posix, Linux; if nt, Windows
    password = ''  # The EnKryptos key information will be inserted here
    keyPass = '[REDACTED]'  # This handles key encryption
    invalid = ['!', '@', '#', '$', '%',
               '^', '&', '*', '(', ')',
               '+', '=', '\\', '/', ':'
               ';', '"', "'", '<', '>',
               '?', '|', '{', '}']  # Special symbols that are not allowed in naming messages

    def __init__(self, master=None):
        # 1. Get or create key
        if os.path.isfile('key/key.EDK'):  # If we've got a key already
            # 1. Decrypt key and assign contents to password
            bit = 64 * 1024
            key = fakeFile()
            messageMod.decryptFile('key/key.EDK', key, self.keyPass, bit)
            self.password = key.getvalue()

            # 2. Prevent leak of key info
            key.close()  # Closing of fake files done to prevent keyPass from being discovered (hacker defense)

            # 3. Recognize that this is not the first boot
            firstBoot = False

        else:  # If we don't have a key
            # 1. Randomly create one
            self.password = self.randGen(size=500)  # This is admittedly gratuitous, but I like it like this

            # 2. Save to fake file
            self.folderExists(type='key')

            ramFile = fakeFile()
            ramFile.write(self.password)

            # 3. Encrypt message and save to .aes file in encryption folder
            bit = 64 * 1024
            try:
                # print('Attempting to call function.')
                messageMod.encryptFile(ramFile, 'key/key.EDK', self.keyPass, bit)
                ramFile.close()
            except:
                ramFile.close()  # If something goes wrong, immediately close file to prevent key being discovered

            # 4. Recognize that this is probably the first boot
            firstBoot = True

        # 2. Build ui
        self.MainFrame = tk.Frame(master)

        # Encrypt File Button
        self.encrypt_button = ttk.Button(self.MainFrame)
        self.encrypt_button.config(text='Encrypt File')
        self.encrypt_button.place(anchor='nw', height='50', relx='0.05', rely='0.15', width='200', x='0', y='0')
        self.encrypt_button.configure(command=lambda: self.workCrypt(operation='encrypt'))

        # Decrypt File Button
        self.decrypt_button = ttk.Button(self.MainFrame)
        self.decrypt_button.config(text='Decrypt File / Message')
        self.decrypt_button.place(anchor='nw', height='50', relx='0.05', rely='0.36', width='200', x='0', y='0')
        self.decrypt_button.configure(command=lambda: self.workCrypt(operation='decrypt') )

        # Message Subject Text Entry (sets file name)
        self.messageName = ttk.Entry(self.MainFrame)
        _text_ = '''Enter Message Title'''
        self.messageName.delete('0', 'end')
        self.messageName.insert('0', _text_)
        self.messageName.place(anchor='nw', height='25', relx='0.46', rely='.03', width='200', x='0', y='0')

        # Encrypt Message Button
        self.Encrypt_Text = ttk.Button(self.MainFrame)
        self.Encrypt_Text.config(text='Encrypt Message')
        self.Encrypt_Text.place(anchor='nw', relx='0.46', rely='0.56', x='0', y='0')
        self.Encrypt_Text.config(command=lambda: self.workCrypt(operation='message'))

        # Message Content Entry (content will be encrypted)
        self.Secret_Message = tk.Text(self.MainFrame)
        self.Secret_Message.config(height='10', width='50', wrap='word')
        _text_ = '''Enter Message to Encrypt'''
        self.Secret_Message.insert('0.0', _text_)
        self.Secret_Message.place(anchor='nw', height='115', relx='0.46', rely='0.15', width='300', x='0', y='0')

        # Separator
        self.separator_1 = ttk.Separator(self.MainFrame)
        self.separator_1.config(orient='vertical', takefocus=False)
        self.separator_1.place(anchor='nw', height='197', relx='0.43', rely='0.0', width='3', x='0', y='0')

        # Label For Message Creator
        self.label_mess = ttk.Label(self.MainFrame)
        self.label_mess.config(text='Create Encrypted\n       Message')
        self.label_mess.place(anchor='nw', relx='0.81', rely='0.03', x='0', y='0')

        # Label For File Encryptor / Decryptor
        self.label_file = ttk.Label(self.MainFrame)
        self.label_file.config(text='Encrypt or Decrypt Individual Files')
        self.label_file.place(anchor='nw', relx='0.06', rely='.03', x='0', y='0')

        # Separator
        self.separator_1_2 = ttk.Separator(self.MainFrame)
        self.separator_1_2.config(orient='horizontal')
        self.separator_1_2.place(anchor='nw', rely='0.65', width='600', x='0', y='0')

        # Message / Feedback Display Window
        self.decryView = tk.Text(self.MainFrame)
        self.decryView.config(height='10', state='disabled', width='50', wrap='word')
        self.decryView.place(anchor='nw', height='75', relx='0.01', rely='0.73', width='575', x='0', y='0')

        # Label For Display Window
        self.label_1 = ttk.Label(self.MainFrame)
        self.label_1.config(text='Decrypted Message / Notification Viewer')
        self.label_1.place(anchor='nw', relx='0.01', rely='.66', x='0', y='0')

        # Scrollbars
        self.scrollbar_view = ttk.Scrollbar(self.MainFrame)  # This is the display window's scrollbar
        self.scrollbar_view.configure(orient='vertical')
        self.scrollbar_view.place(anchor='nw', height='75', relx='.97', rely='.73', x='0', y='0')
        self.scrollbar_view.configure(command=self.decryView.yview)

        self.scrollbar_messEnter = ttk.Scrollbar(self.MainFrame)  # This is the message text entry scrollbar
        self.scrollbar_messEnter.configure(orient='vertical')
        self.scrollbar_messEnter.place(anchor='nw', height='115', relx='.96', rely='.15', x='0', y='0')
        self.scrollbar_messEnter.configure(command=self.Secret_Message.yview)

        # GUI Config
        self.MainFrame.config(height='300', relief='flat', takefocus=False, width='600')
        self.MainFrame.pack(side='top')

        # Main widget
        self.mainwindow = self.MainFrame

        # 3. Give welcome message
        if firstBoot:
            self.changeText(text=('Welcome to EnKryptos! Be sure to check out the readme.txt file ' +
                                  'for more information on how to use this application. Use with ' +
                                  'caution and remember that by using EnKryptos you\'re effectively agreeing to the ' +
                                  'included disclaimer.txt file. Happy encrypting!'))



    # ================================================
    # ================================================
    # ========== Redirection / Threads ===============
    # ================================================
    # ================================================
    # => This function acts as a way-station that
    # creates threads as it redirects to the specified
    # functions. It is given its own section as it is
    # rather verbose


    def workCrypt(self, operation):  # This function calls threads for processes to prevent freezing
        if operation == 'encrypt':  # If we're encrypting a file
            if not self.workLock:  # If nothing is currently being processed
                file = filedialog.askopenfilename(initialdir=self.homeDir, title='Select a File to Encrypt',
                                                  filetypes=(("All Files", "*.*"), ('Text', '*.txt')))

                if not os.path.isfile(str(file)):  # If there's no path, the user exited out. Abort.
                    return

                self.changeText(text='Working on encryption, please stand by.')
                process = threading.Thread(target=lambda: self.encrypt(pathway=file))  # Create function thread
                process.start()  # Start function thread

            else:  # If something is being processed, ignore command
                return

        elif operation == 'decrypt':  # If we're decrypting a file
            if not self.workLock:
                # 1. Ensure that an encrypted_files directory exists
                self.folderExists(type='encrypt')  # If the encrypted files folder does not exist make it
                if self.opSys == 'nt':  # If OS == Windows
                    folder = self.homeDir + '\\encrypted_files'

                else:  # If OS == Linux-based
                    folder = self.homeDir + '/encrypted_files'

                # 2. Get pathway to .aes file
                file = filedialog.askopenfilename(initialdir=folder, title='Select a File to Decrypt',
                                                     filetypes=(("Encrypted Files", "*.aes"), ('Invalid Files', '*.*')))

                # 3. Determine if this is a valid file to decrypt
                if not os.path.isfile(str(file)):  # If there's no valid path, the user exited out. Abort.
                    return
                self.changeText(text='Working on decryption, please stand by.')
                process = threading.Thread(target=lambda: self.decrypt(pathway=file))
                process.start()

            else:
                return

        elif operation == 'message':  # If we're creating an encrypted message
            if not self.workLock:  # This doesn't require verification as message-creation is handled in-app
                process = threading.Thread(target=self.encryptMessage)  # Doesn't use lambda as no arguments are passed
                process.start()

            else:
                return

    # ================================================
    # ================================================
    # ========== Encryption / Decryption =============
    # ================================================
    # ================================================
    # => These are the functions needed for encryption
    # and decryption services


    def encrypt(self, pathway):  # This function will encrypt files
        try:
            # 1. Obtain worklock and get relevant information from pathway
            self.workLock = True
            extension = self.getPathExt(path=pathway)  # Process the path: get the extension
            fileName = self.getName(path=pathway, encrypt=True)  # Identify the name of the file

            # 2. Determine if user is trying to re-encrypt an already encrypted file. If so, abort.
            if extension == '.aes' or extension == '.EDK':
                self.changeText(text='ERROR: Process Aborted\nREASON: Attempt to encrypt already encrypted file')
                self.workLock = False
                return

            # 3. Begin encryption and properly save file
            if pathway != '' and pathway != 'No File Selected':  # If we've got a valid path, begin operation.
                bit = 64 * 1024
                self.folderExists(type='encrypt')
                pyAesCrypt.encryptFile(pathway, 'encrypted_files/' + fileName + extension + '.aes',
                                       self.password, bit)

            self.changeText(text='File Successfully Encrypted!')

        except Exception as e:  # If something goes wrong, alert user and exit the function.
            self.changeText(text='ERROR: Encryption Failed\nREASON: ' + str(e))
            self.workLock = False

        # Release Worklock
        self.workLock = False


    def decrypt(self, pathway):  # This function will decrypt files
        try:
            # 1. Obtain worklock and identify current file extension
            self.workLock = True
            extension = self.getPathExt(path=pathway)  # Store the current extension of the file

            if extension != '.aes' and not extension == '.EDK':  # If current file is not encrypted, abort
                self.changeText(text='ERROR: Process Aborted\nREASON: Attempt ' +
                                     'to decrypt a file that\'s either unencrypted or encrypted with another app')
                self.workLock = False
                return

            elif extension == '.EDK':  # If file is EDK, refuse access
                self.changeText(text='ERROR: Access Denied\nREASON: Attempt ' +
                                     'to decrypt EnKryptos decryption key')
                self.workLock = False
                return

            # 2. Identify pre-encryption filetype
            oldExten = self.getOldExt(pathway)
            if oldExten == '.msg':  # Detect if file is an EnKryptos message
                isMessage = True
            else:
                isMessage = False

            # 3. Identify the name of the file
            fileName = self.getName(path=pathway, encrypt=False)

            # 4. Begin decryption process
            if not isMessage:  # If the file is not a msg file, decrypt normally
                if pathway != '' and pathway != 'No File Selected':
                    bit = 64 * 1024
                    self.folderExists(type='decrypt')
                    pyAesCrypt.decryptFile(pathway, 'decrypted_files/' + fileName + oldExten, self.password, bit)
                    self.changeText(text='File (' + oldExten + ') Successfully Decrypted!')

            else:  # If the file is an msg file, decrypt using fake file and output data to display window
                if pathway != '' and pathway != 'No File Selected':
                    bit = 64 * 1024
                    outputF = fakeFile()
                    messageMod.decryptFile(pathway, outputF, self.password, bit)
                    self.changeText(text=outputF.getvalue())
                    outputF.close()  # Close fake file for hacking defense

        except:
            self.changeText(text='ERROR: Decryption Failed\nREASON: ' +
                                 'Either the wrong key is inserted or the file is corrupted')
            self.workLock = False

        self.workLock = False  # Release worklock


    def encryptMessage(self):  # This function will encrypt a new message
        self.workLock = True
        # 1. Get message contents, determine if name is valid (if not, clean it)
        toEncode = self.Secret_Message.get("1.0", "end-1c")  # Gets message content
        subject = self.messageName.get()  # Gets message title

        # 1.1 Easter Eggs or test codes
        isJoke = self.easterEgg(code=subject)  # Returns a bool
        if isJoke:
            joke = True

        else:
            joke = False

        # 1.2 Clean invalid names

        for item in self.invalid:  # Look at every invalid symbol
            for char in subject:  # Look at every character in the name
                if item in char:  # If an invalid symbol is found at the character position
                    subject = subject.replace(char, '')  # Replace it with an empty character

        # 2. Save to fake file
        ramFile = fakeFile()
        ramFile.write(toEncode)

        # 3. Encrypt message and save to .aes file in encryption folder
        bit = 64 * 1024
        self.folderExists(type='encrypt')
        try:
            messageMod.encryptFile(ramFile, 'encrypted_files/' + subject + '.msg.aes', self.password, bit)

            if not joke:  # If user didn't enter a joke code, don't override the display window
                self.changeText(text='Encrypted Message Successfully Created!')
                self.changeText(text='', ee=True)  # Use easter egg functionality to wipe text entry

            else:
                self.changeText(text='You\'ve been hit by, you\'ve been struck by, a smooth criminal!\n\n' +
                                     '(Btw, your message was encrypted)')
        except Exception as e:
            self.changeText(text='ERROR: Encryption Failed\nREASON: ' + str(e))  # Show what went wrong
            self.workLock = False

        ramFile.close()  # Always close files, fake or not, for hacking defense
        self.workLock = False




    # ================================================
    # ================================================
    # ========== File Creation and Organization ======
    # ================================================
    # ================================================
    # => These functions handle folder creation, file
    # interpretations, and random generation (for EDK
    # files and 'test random' display)


    def getName(self, path, encrypt):  # This function will determine the name of files
        name = []  # Empty list predefined for appending
        periodCt = 0  # This variable will hold the number of encountered periods
        pos = -1  # This will be our index as we iterate backwards
        trigger = 0  # This tells us when to stop iterating through the path

        # 1. Determine if the operation is decryption or encryption, set appropriate trigger
        if encrypt:
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


    def getPathExt(self, path):  # This function will determine the extension of unencrypted files
        position = -1  # Index as we iterate backwards
        extension = []  # Empty list for appending

        # 1. Append the list until a period has been encountered
        while True:
            if path[position] != '.':
                extension.append(path[position])
                position -= 1
            else:
                extension.append('.')
                break

        # 2. Correct list orientation, then compile into string
        extension.reverse()

        exten = ''
        exten = exten.join(extension)
        return exten



    def getOldExt(self, path):  # This function will get the old extension of encrypted files
        position = -1  # This will be our index as we iterate backwards
        extension = []  # Empty list predefined for appending
        perCt = 0  # This tells us how many periods we've encountered

        # 1. Iterate backwards until a period has been passed, then append
        #    the list until the second period is encountered (format = .old.aes)

        # Holy shit, this should be so much simpler. I would change it, but it works, I don't remember how it works,
        # and I'm too lazy to spend some time analyzing it to beautify it. Maybe I'll beautify it later.
        while True:
            if path[position] != '.' and perCt == 0:
                position -= 1

            elif path[position] == '.' and perCt == 0:
                perCt = 1
                position -= 1

            elif path[position] != '.' and perCt == 1:
                extension.append(path[position])
                position -= 1

            elif path[position] == '.' and perCt == 1:
                extension.append('.')
                break

            else:
                position -= 1

        # 2. Correct list orientation, assign the extension string to exten, then return exten
        extension.reverse()

        exten = ''
        exten = exten.join(extension)
        return exten


    def randGen(self, size):  # This function will randomly generate text
        randName = []
        numOrChar = randint(0, 3)
        specialCt = len(self.invalid) - 1  # Size of the list containing special characters

        # 1. Randomly generate text until character length (size) is met
        for char in range(size):
            if numOrChar == 0:  # Use Number
                randName.append(chr(randint(48, 57)))

            elif numOrChar == 1:  # Use Lowercase Character
                randName.append(chr(randint(97, 122)))

            elif numOrChar == 2:  # Use Special Character
                randName.append(self.invalid[randint(0, specialCt)])
                if randName[-1] == "'" or randName[-1] == '"':
                    randName[-1] = '*'

            else:  # Use Capitalized Character
                randName.append(chr(randint(65, 90)))

            numOrChar = randint(0, 3)  # Reset the chance

        # 2. Convert the list into a single string and return it
        gen = ''
        gen = gen.join(randName)

        return gen


    def folderExists(self, type):  # Determine if the folder exists. If not, make it.
        if type == 'encrypt':
            if os.path.exists('encrypted_files/'):
                pass
            else:
                os.mkdir('encrypted_files/')

        elif type == 'decrypt':
            if os.path.exists('decrypted_files/'):
                pass
            else:
                os.mkdir('decrypted_files/')

        elif type == 'key':
            if os.path.exists('key/'):
                pass
            else:
                os.mkdir('key/')



    # ================================================
    # ================================================
    # ========== Misc. ===============================
    # ================================================
    # ================================================
    # => These functions perform tasks that do not fall
    # into one of previously defined groups


    def easterEgg(self, code):  # Determine if the inputted code calls an easter egg
        # 1. Dispense appropriate response
        if code == 'rick roll' or code == 'Rick roll':
            quote = ("We're no strangers to love\n" +
                     "You know the rules and so do I\n" +
                     "A full commitment's what I'm thinking of\n" +
                     "You wouldn't get this from any other guy\n\n" +
                     "I just wanna tell you how I'm feeling\n" +
                     "Gotta make you understand\n\n" +
                     "Never gonna give you up\n" +
                     "Never gonna let you down\n" +
                     "Never gonna run around and desert you\n" +
                     "Never gonna make you cry\n" +
                     "Never gonna say goodbye\n" +
                     "Never gonna tell a lie and hurt you")

            self.changeText(text=quote, ee=True)
            return True

        elif code == 'test random':
            output = ''
            for x in range(27):
                output += self.randGen(size=randint(4, 16)) + '.' + self.randGen(size=(randint(3, 7))) + '\n'

            self.changeText(text=output, ee=True)
            return True

        elif code == 'Harambe' or code == 'harambe':
            praise = ('Blessed be His name,\n' +
                      'He who involuntarily died for our sins,\n' +
                      'And set everything in motion.\n\n' +
                      '--Dicks Out For Harambe--')
            self.changeText(text=praise, ee=True)
            return True

        elif code == 'EnKryptos':
            quote = ("In this age of communications that span both distance and time, the only tool we have that " +
                     "approximates a 'whisper' is encryption. When I cannot whisper in my wife's ear or the ears of " +
                     "my business partners, and have to communicate electronically, then encryption is our tool to " +
                     "keep our secrets secret.\n\n-- John McAfee")
            self.changeText(text=quote, ee=True)
            return True

        else:  # If no appropriate response was found, this is not a valid code
            return False


    def changeText(self, text, ee=False):  # Gets text and prints it to textbox (ee = easter egg)
        if not ee:  # If not an easter egg, print in display window
            self.decryView.config(state='normal')
            self.decryView.delete('1.0', 'end')
            self.decryView.insert('0.0', text)
            self.decryView.config(state='disabled')

        else:  # Else, print in text entry
            self.Secret_Message.delete('1.0', 'end')
            self.Secret_Message.insert('0.0', text)


    def run(self):
        self.mainwindow.mainloop()


if __name__ == '__main__':
    import tkinter as tk
    root = tk.Tk()
    root.resizable(height=False, width=False)  # Prohibit resizing the height or width of window
    root.wm_title("EnKryptos v0.3.4")  # Sets the title of the window to the string included as an argument

    app = EnKryptosGUI(root)
    app.run()
