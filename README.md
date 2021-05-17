# EnKryptos
***By using EnKryptos, you agree to use it at your own risk, hold me free of any responsiblilty should any kinds of loss or damage occur, and only use it on information you either own or have explicit permission to encrypt. This program will encrypt files, so if you use it negligently you could permanently lose access to your information. Be sure to use EnKryptos intelligently and with caution.***

Encryption enables communication among adversaries. With EnKryptos, your encrypted files and messages will be virtually unbreakable. This application uses the AES encryption protocol (a cipher approved by the U.S. National Security Agency (NSA) for protecting top-secret information) with a random key of 500 character length.

# EnKryptos v0.3.1 Changelog

- Added special keys. They will dramatically enhance encrypted file security.

- Added more feedback messages communicated via the display window.

- Expanded pyAesCryptMod to allow the decryption of messages without creating a dedicated unprotected file on the hard-drive. 

# Using Enkryptos as an Executable (Strong Encryption Strength)

Strenghth Reason: random keys are generated on first start up. Even if an adversary knew about EnKryptos and had their own copy, they wouldn't be able to decrypt your files without somehow getting access to your particular special key. Keep your key secure and your files will be virtually unbreakable. With each random key being 500 characters long and containing random placements of upprcase and lowercase characters, numbers, and special characters, it would effectively take an infinite amount of time to brute force your password. With EnKryptos Decryption Keys, your files will be ultra-secure.

As an executable, all you'll need to do to get started is download the EnKryptos-Win.zip or EnKryptos-Lin.tar.gz files (for Windows and Linux, respectively) included in this repository. This is the way EnKryptos is intended to be commonly used.

Extract it and do the following:

**Windows:**

After extracting the zip, find the EnKryptos.exe file within the new folder and double click to run. Don't move the executable from its folder -- there's a lot of necessary parts hidden within the folder (makes it easier for you to find the right file).

**Linux:**

After extracting the tarball, cd into the extracted folder. Locate the EnKryptos file and use "./EnKryptos" to execute it. 

# Using Enkryptos as a Script 

**Steps:**

1. Ensure you have Python 3.8 or greater installed.
2. pip install pyAesCrypt and tkinter (if your Python version does not already have this installed).
3. Download main.py and pyAesCryptMod.py. Put both files in the same directory.
4. Open main.py with a text editor. Replace the keyPass variable assignment with a long random password.
5. Run main.py with Python.


# Notes

- Keys are unique and non-recoverable. If you somehow lose your key, your encrypted files will made useless clusters of obfuscated data. Do not lose your key.
