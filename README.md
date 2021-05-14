# EnKryptos
***By using EnKryptos, you agree to use it at your own risk, hold me free of any responsiblilty should any kinds of loss or damage occur, and only use it on information you either own or have explicit permission to encrypt. This program will encrypt files, so if you use it negligently you could permanently lose access to your information. Be sure to use EnKryptos intelligently and with caution.***

EnKryptos is an application for encrypting and decrypting files using the AES encryption protocol. With a secret key encoded in 
the executable file, this application will be the only way you can decrypt EnKryptos-encrypted files or 
messages. 

Encryption enables communication among adversaries. As long as they not aware of the existence of this 
application, your encrypted files should be virtually unbreakable. If they are aware of EnKryptos,
you can use the script-version to implement a custom secret key to provide you with the most peace of
mind and security.

# EnKryptos v0.3 Changelog

- Added a decrypted message / notification viewer.

- Eliminated a hacking vulnerability by circumventing the need to create an unencrypted file during message encryption.

- Added notifications that inform you when a process has been aborted and why it was aborted.

# Using Enkryptos as an Executable (Weak to Normal Encryption Strength)

Strenghth Reason: since the secret key is encoded into the executable file, an adversary aware of EnKryptos could simply use their own copy to decrypt the file. Since this program is still relatively unknown, this shouldn't be too large an issue for standard use. If you want to encrypt files with the best security possible, I'd recommend running it as a script instead.

As an executable, all you'll need to do to get started is download the EnKryptos-win.zip or EnKryptos-Lin.tar.gz files (for Windows and Linux, respectively) included in this repository. 

Extract it and do the following:

**Windows:**

Find the EnKryptos.exe file within and double click to run. Don't move the executable from its folder -- there's a lot of necessary parts
hidden within the folder (makes it easier for you to find the right file).

**Linux**

After extracting the tarball, cd into the extracted folder. Locate the EnKryptos file and use "./EnKryptos" to execute it. 

# Using Enkryptos as a Script (Strong Encryption Strength)

Strength Reason: since the script will require that you use a custom secret key, it should be nearly impossible for an adversary to decrypt EnKryptos-encrypted files, regardless of their knowledge of this program. In order to discover your secrets, they'd need to learn your secret key or install some kind of advanced spyware that intercepts information before you have a chance to encrypt it. (Note: adversaries could learn how to decrypt your files if they hack you and get access to the script file, which contains your secret key. One possible solution to this, off the top of my head, is to keep the script on a USB and transfer your encrypted files to some other storage medium immediately after encryption (keep the encrypted files away from the script until you need to decrypt them).)

**Steps:**

0. Ensure you have Python 3.8 or greater installed.

1. pip install pyAesCrypt and tkinter (if your Python version does not already have this installed)
2. Download sourcecode and pyAesCryptMod. Put both files in the same directory.
3. Open the sourcecode in your preferred text editor.
4. Locate the variable 'password', delete its '[REDACTED]' assignment, and enter a new very long random password 
   as a string. This password should contain special characters, upper and lower case letters, and numbers. Example password: "Rg^%ccat4@@bcws6UMb!PaG&11796#bvarTipU0c%^\*" (do not use this as your password).
6. Save and run.


# Notes

- The update provides partial spyware protection. With it, an adversary scanning your files won't be able to 
intercept your unencrypted messages. This doesn't mean that interception is impossible, only that it is 
significantly more difficult and would require more advanced spyware (or a keylogger, but in that case 
you're fucked regardless). Moral of the story: don't get hacked, but if you do, EnKryptos should offer 
*a little* protection for your messages.
