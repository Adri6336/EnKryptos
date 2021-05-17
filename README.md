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

- Added keys. Keys will dramatically enhance encrypted file security.

- Added more feedback messages via the display window.

- Expanded pyAesCryptMod to allow the decryption of files without creating a dedicated file on the hard-drive. 

# Using Enkryptos as an Executable (Strong Encryption Strength)

Strenghth Reason: random keys are generated on first start up. Even if an adversary knew about EnKryptos and had their own copy, they wouldn't be able to decrypt. 

As an executable, all you'll need to do to get started is download the EnKryptos-win.zip or EnKryptos-Lin.tar.gz files (for Windows and Linux, respectively) included in this repository. 

Extract it and do the following:

**Windows:**

After extracting the zip, find the EnKryptos.exe file within the new folder and double click to run. Don't move the executable from its folder -- there's a lot of necessary parts hidden within the folder (makes it easier for you to find the right file).

**Linux:**

After extracting the tarball, cd into the extracted folder. Locate the EnKryptos file and use "./EnKryptos" to execute it. 

# Using Enkryptos as a Script 

**Steps:**

0. Ensure you have Python 3.8 or greater installed.

1. pip install pyAesCrypt and tkinter (if your Python version does not already have this installed)
2. Download sourcecode and pyAesCryptMod. Put both files in the same directory.
3. Run with Python.


# Notes

- The update provides partial spyware protection. With it, an adversary scanning your files won't be able to 
intercept your unencrypted messages. This doesn't mean that interception is impossible, only that it is 
significantly more difficult and would require more advanced spyware (or a keylogger, but in that case 
you're fucked regardless). Moral of the story: don't get hacked, but if you do, EnKryptos should offer 
*a little* protection for your messages.
