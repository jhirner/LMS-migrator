# LMS Migrator
A tool for educators. Easily update due dates from previous terms' Common Cartridge file.

## Who is this for?
LMS Migrator is designed for educators who have better things to do than click a million buttons to update their online classrooms.

## What does it do?
LMS Migrator looks for a previous term's course content, which you can export and download from your LMS as a Common Cartridge (.imscc) file.

The script unpacks the contens of your old course, updating basic metadata like assignment names, availability dates, and due dates according to what you specify in a stripped-down syllabus. It then re-bundles the updated course as a new Common Cartridge file, which is ready for you to upload back to your LMS.

It features a simple, user-friendly interface:
![Screenshot of LMS Migrator window on Mac OSX](webassets/osx_1-1-1_screenshot.png?raw=true)

## Is it compatable with my LMS?
Right now, LMS Migrator has only been tested with the [Canvas LMS](https://www.instructure.com/canvas/) using Common Cartridge version 1.1.0. It *ought* to work with other LMS platforms such as [Blackboard](https://www.blackboard.com/teaching-learning/learning-management), too, but it has not been tested yet. **please give LMS Migrator a try using other LMS platforms and [reach out](#reaching-out) to let us know how it works.**

## Installation
Download *lms_migrator.py* and the template *new_syllabus.xlsx* to a directory of your choice on your computer. 

If you prefer, there are also pre-built executable programs in the [*binaries*](binaries) directory. Although this is the easiest-to-use solution, the executables may not be compatable with your system. If you're comfortable running a Python script from a command line, that is the recommended method. Otherwise, give the pre-built executables are the way to go.

## But really, how do I install it?
You have options! You may directly use LMS Migrator *via the Python script* (Option A, below), or you may install it *using one of the pre-built executable programs* (Option B, below). The former guarantees you the most up-to-date version of LMS Migrator, and it is more likely to work on your system. The latter offers easier installation, but it may not perform as well.

**Option A: Installing the LMS Migrator Python script**. The vanilla installation directions above under "Installation" are the bare-basics. Here are some more detailed directions.

1. *Determine if your computer has Python 3 installed.* This will provide the interpreter that's required to run LMS Migrator.
	* You can do that by opening a terminal or command line and typing `python3`, followed by the enter key.
	* If Python isn't installed, you will receive an error message. It may include instructions for installing Python 3 on your computer.
	* If you don't receive an error, that means Python is already on your computer! Simply enter `quit()` to exit out of Python again.
2. *Install the supporting programs.* LMS Migrator requires the help of a few other Python-based tools to work. You can easily install them by copying/pasting the code below into your terminal / command line prompt. To ensure compatability, we'll specify the exact versions of these tools that were used in developing LMS Migrator. If you already have any of these installed, other versions will likely work, too.
```
pip3 install beautifulsoup4==4.9.3 lxml==4.5.0 openpyxl==3.0.5
```
3. *That's it!* If you didn't receive any error messages along the way, you should be all set. See the directions under *How do I use it?* to continue.

**Option B: Installing LMS Migrator via a Pre-Built Executable**
1. Navigate to the [*binaries*](binaries) folder above. Download the version of LMS Migrator that is best suited for your computer. Currently pre-built executables are available for Mac OSX and Ubuntu. (Sorry, but there is no pre-built executable available at this time for Windows 10. However, you can still run LMS Migrator directly from the Python script, *Option A*, above.)
2. Double-click to unpack the program and save it to any folder you can conveniently find again.
2. *That's it!* You're ready to go. See the directions under *How do I use it?* to continue.

## How do I use it?
Make sure the program and its requirements are installed (see [*Installation*](#installation) and [*But really, how do I install it?*](#but-really-how-do-i-install-it).
1. It's recommended to make a new folder on your computer to keep things tidy & make sure your files are safe. You can call it anything you want, but let's use `lms_migrator` for clarity. **Important:** Always back up your course files before using LMS Migrator!
2. Your new folder needs to have two files in it:
	* The Common Cartridge export (.imscc file) from your previous semester's course, which you can download from your LMS.
		* Although you can use any file name you want, it may make your workflow more straightforward to rename the file you download from your LMS to *old_course.imscc*.
		* Not sure how to export your course? Click for directions using [Canvas](https://community.canvaslms.com/t5/Instructor-Guide/How-do-I-export-a-Canvas-course/ta-p/785) or [Blackboard](https://help.blackboard.com/Learn/Administrator/Hosting/Course_Management/Common_Cartridge_Course_Packages#download-the-course-package_OTP-8).
		* If you given a choice, please select "IMS Common Cartridge v 1.1.0"; LMS Migrator has not yet been tested with other versions of the Common Cartridge format.
	* An Excel spreadsheet that contains a simplified syllabus. **Be sure you follow the template that's provided in the `templates` folder above!**
		* Again, although you can use any file name you want, it might make your life easier to use something simple & clear like *new_syllabus.xlsx*.

**If you're using the LMS Migrator Python script:**

3. Open a command line / terminal and navigate to the folder `lms_migrator` (or whatever you decided to name it) where LMS Migrator, your syllabus, and the old course materials are stored.

4. Type the following in exactly, or simply copy/paste it. `python3 lms_migrator.py`

5. Hit enter and let the program run. Take note of any messages it displays.

**If you're using LMS Migrator via one of the pre-built executable files.**

3. Navigate to the folder where you saved the LMS Migrator application.

4. Double-click the icon to run the program. It may be a little sluggish; that's normal!
	* *Mac OSX users:* You may receive a warning window that says "lms_migrator cannot be opened because the developer cannot be verified." This error arises because Apple charges software developers for 'verification', but LMS Migrator is free & open source. You can still run the program by overriding the warning with [a few simple steps](https://support.apple.com/en-za/guide/mac-help/mh40616/mac).

5. Follow the prompts to update your course. Take note of any messages the program displays.

**Either way, you're essentially done.**

6. Upload the updated Common Cartridge file to your LMS. **Important:** Always double-check that names, due dates, and other parameters were modified the way that you expected.

7. That's it! Feel free to reach out if you have any feedback!

## Reaching out
If you find LMS Migrator valuable, or if you're interested in contributing, please reach out to say so. Contact information is listed on [the author's GitHub page](https://github.com/jhirner).
