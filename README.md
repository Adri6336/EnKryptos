# EnKryptos
***By using EnKryptos, you agree to use it at your own risk, hold me free of any responsiblilty should any kinds of loss or damage occur, and only use it on information you either own or have explicit permission to encrypt. This program will encrypt files, so if you use it negligently you could permanently lose access to your information. Be sure to use EnKryptos intelligently and with caution.***

Encryption enables communication among adversaries. With EnKryptos, your encrypted files and messages will be virtually unbreakable. This application uses the AES encryption protocol (a cipher approved by the U.S. National Security Agency (NSA) for protecting top-secret information) with a random key of 500 character length.

# EnKryptos v0.3.2 Changelog

- Deleted vestigial code

- Removed the global-like temp variables and replaced it with local variables 

- Slightly cleaned code

- Made decryption button automatically open your encrypted_files folder

- Made encrypted messages clear upon succesful encryption

- Added and edited notes

- Added easter egg


# Using Enkryptos as an Executable (Strong Encryption Strength)

Strenghth Reason: random keys are generated on first start up. Even if an adversary knew about EnKryptos and had their own copy, they wouldn't be able to decrypt your files without somehow getting access to your particular special key. Keep your key secure and your files will be virtually unbreakable. With each random key being 500 characters long and containing random placements of upprcase and lowercase characters, numbers, and special characters, it would effectively take an infinite amount of time to brute force your password. With EnKryptos Decryption Keys (EDK), your files will be ultra-secure.

As an executable, all you'll need to do to get started is download the EnKryptos-Win.zip or EnKryptos-Lin.tar.gz files (for Windows and Linux, respectively) included in this repository. This is the way EnKryptos is intended to be commonly used.

Extract it and do the following:

**Windows:**

After extracting the zip, find the EnKryptos.exe file within the new folder and double click to run. Don't move the executable from its folder -- there's a lot of necessary parts hidden within the folder (makes it easier for you to find the right file).

**Linux:**

After extracting the tarball, cd into the extracted folder. Locate the EnKryptos file and use "./EnKryptos" to execute it. 

# Using Enkryptos as a Script (Ultra Strength)

Strength Reason: since the script demands a custom keyPass assignment, your files will have two levels of personalized encryption. The first level: keys will be encrypted with a special user-defined password (these keys will only work with other script-versions of EnKryptos with the equivalent keyPass assignment); the second level: your random EDK key will be used to encrypt and decrypt files and messages. Even if an adversary stole your EDK file, they wouldn't be able use it to decrypt your files unless they also stole your EnKryptos copy with the correct keyPass assignment.

**Steps:**

1. Ensure you have Python 3.8 or greater installed.
2. pip install pyAesCrypt and tkinter (if your Python version does not already have this installed).
3. Download main.py and pyAesCryptMod.py. Put both files in the same directory.
4. Open main.py with a text editor. Replace the keyPass variable assignment with a long random password (you can enter the code "test random" in the "Enter Message Title" textbox within the exe version of EnKryptos to get a series of random codes -- use a couple of these).
5. Run main.py with Python.


# Notes

- Keys are unique and non-recoverable. If you somehow lose your key, your encrypted files will made useless clusters of obfuscated data. Do not lose your key.

- Keys created with the script version will not be interoperable with the executable version. If you want to share your key with other parties that are also using the script version, you'll need to give them the value you entered for the keyPass variable; they must use this password as well to decrypt your messages.


# Q&A
Q: How to use EnKryptos to safely send data over the internet?

A: Physically give your key to your intended recipient (via USB, SD card, direct transfer by cable, etc.). You can do this by giving them a copy of your EnKryptos folder in a zip or tar.gz file after you've run EnKryptos at least once (the keys are only generated upon first startup). If you're using the script version, they must recieve a copy of your main.py with the correct custom keyPass assignment. Once they've got an EnKryptos copy with the valid key, you should be good to send encrypted files through email or other internet tools. To maximize privacy, you should use a secure email service like [CTemplar](https://ctemplar.com/) (paid service) or [ProtonMail](https://protonmail.com/) (free).
