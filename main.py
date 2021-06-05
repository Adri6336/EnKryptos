# Basic imports
import tkinter.ttk as ttk  # Needed for gui
from tkinter import filedialog  # Needed to select files
import pyAesCrypt  # Needed for aes encryption and decryption of files
import os  # Needed for creating files, identifying valid paths, and deleting files
import threading  # Allows EnKryptos to run smoother by preventing it from freezing with large files / arduous tasks
from time import sleep  # Allows speed modification of text grow or shrink


# Needed for hacking defense
import gc  # Needed to help clear data from memory
from secrets import randbelow, token_bytes  # Needed for cryptographically secure key generation
from io import StringIO as fakeFile  # Prevents hard-drive files from being created during encryption / decryption
import pyAesCryptMod as messageMod  # Allows me to use pyAesCrypt with StringIO files
from sys import getsizeof as sizeBytes  # Tries to force garbage collection


# Gui created with Pygubu-Designer
class EnKryptosGUI:
    workLock = False  # This prevents more operations from being performed simultaneously
    keyMade = False  # This tells EnKryptos if a key has been created
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

            # 3. Recognize that this is not the first boot and key has been made
            firstBoot = False
            self.keyMade = True


        elif os.path.isfile('key/kc.log') and not os.path.isfile('key/key.EDK'):  # Key was made, but removed
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

            # 4. Recognize that this is probably the first boot and we've made a key, create kc.log file
            firstBoot = True
            self.keyMade = True

            with open('key/kc.log', 'w') as file:
                file.write(self.randGen(size=12))  # Write random junk

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

        # 3. Give welcome message or other startup messages
        if firstBoot and self.keyMade:
            self.changeText(text=('Welcome to EnKryptos! Be sure to check out the readme.txt file ' +
                                  'for more information on how to use this application. ' +
                                  'Remember that you\'re agreeing to the ' +
                                  'included disclaimer.txt file by using EnKryptos. Happy encrypting!'))

        elif not self.keyMade:
            self.changeText(text='Please insert a valid key and restart EnKryptos.')



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
            if not self.keyMade:
                self.changeText('Insert key to encrypt.')
                return

            if not self.workLock:  # If nothing is currently being processed
                file = filedialog.askopenfilename(initialdir=self.homeDir, title='Select a File to Encrypt',
                                                  filetypes=(("All Files", "*.*"), ('Text', '*.txt')))

                if not os.path.isfile(str(file)):  # If there's no path, the user exited out. Abort.
                    return

                process = threading.Thread(target=lambda: self.encrypt(pathway=file))  # Create function thread
                process.start()  # Start function thread

            else:  # If something is being processed, ignore command
                return

        elif operation == 'decrypt':  # If we're decrypting a file
            if not self.keyMade:
                self.changeText('Insert key to decrypt.')
                return

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
                process = threading.Thread(target=lambda: self.decrypt(pathway=file))
                process.start()

            else:
                return

        elif operation == 'message':  # If we're creating an encrypted message
            if not self.keyMade:
                self.changeText('Insert key to create messages.')
                return

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
        self.changeText(text='Working on encryption, please stand by.')
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



        except Exception as e:  # If something goes wrong, alert user and exit the function.
            self.changeText(text='ERROR: Encryption Failed\nREASON: ' + str(e))
            self.workLock = False

        # 4. Try to wipe file from low-level memory
        self.corrupt(target=pathway, isFile=True)


        # Release Worklock, announce success
        self.changeText(text='File Successfully Encrypted!')
        self.workLock = False


    def decrypt(self, pathway):  # This function will decrypt files
        self.changeText(text='Working on decryption, please stand by.')
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
                    self.corrupt(target=pathway, isFile=True)  # Scramble memory
                    self.changeText(text='File (' + oldExten + ') Successfully Decrypted!')



            else:  # If the file is an msg file, decrypt using fake file and output data to display window
                if pathway != '' and pathway != 'No File Selected':
                    bit = 64 * 1024
                    outputF = fakeFile()
                    messageMod.decryptFile(pathway, outputF, self.password, bit)
                    self.growText(content=outputF.getvalue(), wait=0.0005, textEntry=False)  # Animated display
                    delBytes = sizeBytes(outputF)  # Record how large the file was
                    outputF.close()  # Close fake file for hacking defense

                    self.corrupt(target=delBytes, justBytes=True, showActivity=False)  # Scramble memory

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
        self.growText(content=toEncode, wait=0.005, reverse=True)  # Clear message from screen

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

        # 2. Save to fake file, get size
        ramFile = fakeFile()
        ramFile.write(toEncode)
        delBytes = sizeBytes(ramFile)

        # 3. Encrypt message and save to .aes file in encryption folder
        bit = 64 * 1024
        self.folderExists(type='encrypt')
        try:
            messageMod.encryptFile(ramFile, 'encrypted_files/' + subject + '.msg.aes', self.password, bit)


        except Exception as e:
            self.changeText(text='ERROR: Encryption Failed\nREASON: ' + str(e))  # Show what went wrong
            self.workLock = False


        # 4. close message fake file, then try to scramble memory
        ramFile.close()  # Always close files, fake or not, for hacking defense
        self.corrupt(target=delBytes, justBytes=True)  # Scramble memory for hacking defense

        # 5. Dispense easter egg if needed, else display confirmation of succesful encryption
        if not joke:  # If user didn't enter a joke code, don't override the display window
            self.changeText(text='Encrypted Message Successfully Created!')
            #self.changeText(text='', ee=True)  # Use easter egg functionality to wipe text entry

        else:
            self.changeText(text='You\'ve been hit by, you\'ve been struck by, a smooth criminal!\n\n' +
                                 '(Btw, your message was encrypted)')

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
        # Addendum: just received advice from another programmer indicating not to change it since it works
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
        """
        This function will randomly generate text using a cryptographically secure pseudorandom number generator.

        :param size: This indicates how many chars we want to generate.
        """
        randName = []  # Empty list will hold the chars
        numOrChar = randbelow(4)  # Randomly determine what the first char will be
        specialCt = len(self.invalid)  # Size of the list containing special characters

        # 1. Randomly generate text until character length (size) is met
        for char in range(size):
            if numOrChar == 0:  # Use Number
                randName.append(chr(48 + randbelow(10)))  # ASCII Range = 48-57, 10 wont be met so it'll be between 0-9

            elif numOrChar == 1:  # Use Lowercase Character
                randName.append(chr(97 + randbelow(26)))  # 97-122

            elif numOrChar == 2:  # Use Special Character
                randName.append(self.invalid[randbelow(specialCt)])
                if randName[-1] == "'" or randName[-1] == '"' or randName[-1] == '\\':
                    randName[-1] = '*'

            else:  # Use Capitalized Character
                randName.append(chr(65 + randbelow(26)))  # 65-90

            numOrChar = randbelow(4)  # Reset the chance

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

            self.growText(content=quote, wait=0.005)
            return True

        elif code == 'test random':
            output = ''
            for x in range(27):
                output += self.randGen(size=12 + randbelow(25)) + '\n'

            self.growText(content=output, wait=0.001)
            return True

        elif code == 'Harambe' or code == 'harambe':
            praise = ('Blessed be His name,\n' +
                      'He who involuntarily died for our sins,\n' +
                      'And set everything in motion.\n\n' +
                      '--Dicks Out For Harambe--')
            self.growText(content=praise, wait=0.01)
            return True

        elif code == 'EnKryptos':
            quote = ("In this age of communications that span both distance and time, the only tool we have that " +
                     "approximates a 'whisper' is encryption. When I cannot whisper in my wife's ear or the ears of " +
                     "my business partners, and have to communicate electronically, then encryption is our tool to " +
                     "keep our secrets secret.\n\n-- John McAfee")
            self.growText(content=quote, wait=0.01)
            return True

        elif code == 'test fancy':
            response = 'Holy fucking shit, this is smooth as fuck!'
            self.growText(content=response, wait=0.01)
            return True

        else:  # If no appropriate response was found, this is not a valid code
            return False


    def growText(self, content, wait, textEntry=True, reverse=False):
        """
        This function will allow the decorative deletion or insertion of text from the GUI.

        :param content: This is the text data that we'll be manipulating.
        :param wait: This determines how fast the growth/shrink will occur. Means wait per char deletion/addition
        :param textEntry: This tells whether we'll be printing to the text entry or display window. True == TextEntry
        :param reverse: This indicates whether we wish to shrink or grow the text. If reverse is false, the text will
                        grow.
        """
        newStr = ''

        if not reverse:
            for char in content:
                newStr += char
                self.changeText(text=newStr, ee=textEntry)
                sleep(wait)

        else:
            newStr = content  # We'll be deleting newString, so we'll start with it whole and take it down char by char

            while len(newStr) >= 1:  # Do this until we've only got one char left
                self.changeText(text=newStr, ee=textEntry)  # Update text entry with newStr's current state
                newStr = newStr.rstrip(newStr[-1])  # Go to the end of of newStr and strip a char
                sleep(wait)

            self.changeText(text='', ee=textEntry)  # Update textEntry with an empty string
            del newStr


    def changeText(self, text, ee=False):  # Gets text and prints it to textbox (ee = easter egg)
        if not ee:  # If not an easter egg, print in display window
            self.decryView.config(state='normal')
            self.decryView.delete('1.0', 'end')
            self.decryView.insert('0.0', text)
            self.decryView.config(state='disabled')

        else:  # Else, print in text entry
            self.Secret_Message.delete('1.0', 'end')
            self.Secret_Message.insert('0.0', text)


    def corrupt(self, target, isFile=False, justBytes=False, showActivity=True):
        """
        This function is a workaround Python's lack of low-level memory management. I want to delete some data,
        so I'll need to convince Python to delete that info from the RAM by flooding it with random shite. Same
        principal as deleting a file on your HDD and downloading a videogame to ensure corruption of the stuff
        you deleted.

        Might be fruitless, but figured I'd try

        :param target: This is the data that I need to delete from memory.
        :param isFile or justBytes: This will determine how I go about determining the data's byte size.
        :param showActivity: If true, the display window will tell the user that I'm trying to scramble the memory
        """
        if showActivity:
            self.changeText(text='Cleaning data from memory ...')

        if not isFile and not justBytes:  # If target is not a file or byte count, use sizeBytes. Else, inspect the file
            remSize = sizeBytes(target)

        elif isFile:
            remSize = os.stat(target)[6]  # Returns os.stat().st_size, which is the byte size

        elif justBytes:  # If the target is just an integer of bytes, we already know how much to corrupt.
            remSize = target

        else:
            remSize = 64000  # If none of the above are valid, just scramble 64 kb

        try:
            junkBytes = token_bytes(remSize * 40)  # Generate a random token that's 40x as large as the designated size
            del remSize, junkBytes  # Mark it for deletion
            gc.collect()  # Ask Python nicely to try and garbage collect the data

        except Exception as e:
            self.changeText(text='Error encountered while clearing data: ' + str(e))
            del remSize
            gc.collect()
            sleep(5)

    def run(self):
        self.mainwindow.mainloop()


if __name__ == '__main__':
    import tkinter as tk
    root = tk.Tk()
    root.resizable(height=False, width=False)  # Prohibit resizing the height or width of window
    root.wm_title("EnKryptos v0.3.5")  # Sets the title of the window to the string included as an argument

    app = EnKryptosGUI(root)
    app.run()
