# EnKryptos
Application for encrypting and decrypting using the AES encryption protocol. With a secret key encoded in 
the executable file, this application will be the only way you can decrypt EnKryptos-encrypted files or 
messages. 

Encryption enables communication among adversaries. So long as they don't know of the existence of this 
application, your encrypted files will be virtually unbreakable. If they are aware of EnKryptos,
you can use the script-version to implement a custom secret key to provide you with the most peace of
mind.

# EnKryptos v0.3 Changelog

- Added a decrypted message / notification viewer.

- Eliminated a hacking vulnerability by circumventing the need to create an unencrypted file during message encryption.

- Added notifications that inform you when a process has been aborted and why it was aborted.

# Using Enkryptos as an Executable

This application is meant to be used as an executable for most users. If you'd prefer to use it as a 
script, you'll first need to fill in the "[REDACTED]" password with a long random key that includes 
uppercase and lowercase characters, numbers, and special characters.

As an executable, all you'll need to do to get started is download the Enkryptos-win.zip file included in this repository. 
Extract it and do the following:

**Windows:**

Find the EnKryptos.exe file within and double click to run. Don't move the executable from its folder -- there's a lot of necessary parts
hidden within the folder (makes it easier for you to find the right file).

# Using Enkryptos as a Script

1. pip install pyAesCrypt
2. Download sourcecode and pyAesCryptMod. Put both files in the same directory.
3. Open the sourcecode in your preferred text editor.
4. Locate the variable 'password', delete its '[REDACTED]' assignment, and enter a new long random password 
   as a string.
6. Save and run.


# Notes

- The update provides partial spyware protection. With it, an adversary scanning your files won't be able to 
intercept your unencrypted messages. This doesn't mean that interception is impossible, only that it is 
significantly more difficult and would require more advanced spyware (or a keylogger, but in that case 
you're fucked regardless). Moral of the story: don't get hacked, but if you do, EnKryptos should offer 
some protection for your messages.
