# EnKryptos
Application for encrypting and decrypting using the AES encryption protocol. With a secret key encoded in 
the executable file, this application will be the only way you can decrypt EnKryptos-encrypted files or 
messages. 

Encryption enables communication among adversaries. So long as they do not know of the existence of this 
application, your encrypted files will be virtually unbreakable. If they do know of this application,
you can use the script-version to implement a custom secret key to provide you with the most peace of
mind.

# EnKryptos v0.2.1 Changelog

- Improved code organization and notes.

- EnKryptos now stores encrypted and decrypted information in dedicated folders. 

- Improved temporary-file random name generation.

- Added easter egg.

# Using Enkryptos as an Executable

This application is meant to be used as an executable for most users. If you'd prefer to use it as a 
script, you'll first need to fill in the "[REDACTED]" password with a long random key that includes 
uppercase and lowercase characters, numbers, and special characters.

As an executable, all you'll need to do to get started is download the zip file included in this repository. 
Extract it and run the .exe file within. Don't move the executable -- it's got a lot of necessary parts
hidden within the folder (makes it easier for you to find the right file).

# Using Enkryptos as a Script

1. pip install pyAesCrypt
2. Download sourcecode and seed.ksf. Put both files in the same directory.
3. Open the sourcecode in your preferred text editor.
4. Locate the variable 'password', delete its '[REDACTED]' assignment, and enter a new long random password 
   as a string.
6. Save and run.


# Notes

- If you have some kind of spyware installed on your computer, EnKryptos could be compromised despite encrypting 
your files (the information could be intercepted before it gets encrypted). I'm trying to figure out ways to add 
protections against this, but it's rather difficult to maintain a secret when there's an observer seeing you 
come up with the secret in the first place. For the time being, to protect against this vulnerability, try to keep
up good computer practices: don't click on sketchy links, regularly perfom malware scans with services like malwarebytes,
and don't rely on computers that you suspect might be compromised in some way for encrypting important information. Tbh, 
I'm not sure if anyone has come up with a solution to vulnerabilities like this; I'll keep looking into it.
