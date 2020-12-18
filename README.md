# LMS Migrator
A tool for educators. Easily update due dates from previous terms' Common Cartridge.

## Who is this for?
LMS Migrator is designed for educators who have better things to do than click a million buttons to update their online classrooms.

## What does it do?
LMS Migrator looks for a previous term's course content, which you can export and download from your LMS. Use the filename **old_course.imscc** when you save it.

The script unpacks the contens of your old course, updating basic metadata like assignment names, availability dates, and due dates according to what you specify in a stripped-down syllabus. It then re-bundles the updated course as **new_course.imscc**, which is ready for you to upload back to your LMS.

## Is it compatable with my LMS?
Right now, LMS Migrator has only been tested with the [Canvas LMS](https://www.instructure.com/canvas/). Tests with other LMS platforms are pending.

## How do I use it?
Make sure the program and its requirements are installed (see *Installation* and *But really, how do I install it?*).
1. It's recommended to make a new folder on your computer to keep things tidy & make sure your files are safe. You can call it anything you want, but let's use `lms_migrator` for clarity. **Important:** Always back up your course files before using LMS Migrator!
2. Your new folder needs to have 3 files in it:
	* lms_migrator.py, which is where the magic happens.
	* old_course.imscc, the Common Cartridge export of your previous semester's course, which you can download from your LMS.
	* new_syllabus.xlsx, an Excel spreadsheet that contains a simplified syllabus. Be sure you follow the template that's provided here!
3. Open a command line / terminal and navigate to the folder `lms_migrator` (or whatever you decided to name it).
4. Type the following in exactly, or simply copy/paste it. `python3 lms_migrator.py`
5. Hit enter and let the program run. Take note of any messages it displays.
6. Upload *new_course.imscc* to your LMS. **Important:** Always double-check that names, due dates, and other parameters were modified the way that you expected.
7. That's it! Feel free to reach out if you have any feedback!

## Installation
Download `lms_migrator.py` and the template `new_syllabus.xlsx` to a directory of your choice on your computer. That's it.

## But really, how do I install it?
The vanilla installation directions above are the bare-basics. Here are some more detailed directions.
1. **Determine if your computer has Python 3 installed.** This will provide the interpreter that's required to run LMS Migrator.
	* You can do that by opening a terminal or command line and typing `python3`, followed by the enter key.
	* If Python isn't installed, you will receive an error message. It may include instructions for installing Python 3 on your computer.
	* If you don't receive an error, that means Python is already on your computer! Simply enter `quit()` to exit out of Python again.
2. **Install the supporting programs.** LMS Migrator requires the help of a few other Python-based tools to work. You can easily install them by copying/pasting the code below into your terminal / command line prompt. To ensure compatability, we'll specify the exact versions of these tools that were used in developing LMS Migrator. If you already have any of these installed, other versions will likely work, too.
```
pip3 install beautifulsoup4==4.9.3, lxml==4.5.0, openpyxl==3.0.5
```
3. **That's it!** If you didn't receive any error messages along the way, you should be all set. See the directions under *How do I use it?* to continue.
