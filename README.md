# EnKryptos
Application for encrypting and decrypting using the AES encryption protocol. With a secet key encoded in 
the executable file, this application will be the only way you can decrypt EnKryptos-encrypted files or 
messages. 

Encryption enables communication among adversaries. So long as they do not know of the existence of this 
application, your encrypted files will be virtually unbreakable. If they do know of this application,
you can use the script-version to implement a custom secret key to provide you with the most peace of
mind.

# EnKryptos v0.02 Changelog

- Added in-app encrypted message generator. Now you can create encrypted text without having
  to first make an unencrypted copy.
  
- Updated GUI to accommodate both file and message based encryption/decryption.

- EnKryptos now preserves the names of the files it encrypts.

- Buttons now glow when hovered over.

# Using Enkryptos as Executable

This application is meant to be used as an executable for most users. If you'd prefer to use it as a 
script, you'll first need to fill in the "[REDACTED]" password with a long random key that includes 
uppercase and lowercase characters, numbers, and special characters.

As an executable, all you'll need to do to get started is download the zip file included in this repository. 
Extract it and run the .exe file within. Don't move the executable -- it's got a lot of necessary parts
hidden within the folder (makes it easier for you to find the right file).

# Using Enkryptos as Script

1. pip install pyAesCrypt
2. Download sourcecode and random.txt. Put both files in the same directory.
3. Open the sourcecode in your preferred text editor.
4. Locate the variable 'password', delete its '[REDACTED]' assignment, and enter a new long random password 
   as a string.
6. Save and run.
