# Web App Setup Guide

This guide will walk you through the steps to set up the web app on your local machine. 

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- [Git](https://git-scm.com/downloads)
- [VS Code](https://code.visualstudio.com/download)

## Step 1: Clone the GitHub Repository

**if you already cloned the main repositry you can skip this step**

First, you need to clone the repository to your local machine. Open your terminal and run the following command:

```bash
git clone https://github.com/SlimanJammal/LinkedInJobs.git
```


## Step 2: Install Flutter
Next, you need to install Flutter. Follow the instructions based on your operating system:

### <u>macOS</u>
follow this [Link](https://docs.flutter.dev/get-started/install/macos/web)

#### or
Open your terminal and run:

```bash
brew install --cask flutter
```

Add Flutter to your path:
```bash

export PATH="$PATH:`flutter/bin`"
```
### <u>Windows</u>
follow this [Link](https://docs.flutter.dev/get-started/install/windows/web)

#### or
Download the Flutter SDK from Flutter's website.
Extract the zip file and place the contained flutter directory in a desired installation location.
Add the Flutter bin directory to your system path.
### <u>Linux</u>
follow this [Link](https://docs.flutter.dev/get-started/install/linux/web)
## Step 3: Install Flutter Dependencies
Navigate to the project directory (/cv_builder) and run the following command to get the required dependencies:

``` bash
cd LinkedInJobs/cv_builder
flutter pub get
```
If you get the following error:
``` bash
Building with plugins requires symlink support.

Please enable Developer Mode in your system settings. Run
  start ms-settings:developers
to open settings.
```
follow the steps [here.](https://learn.microsoft.com/en-us/windows/apps/get-started/enable-your-device-for-development)

### Step 4: Open the Project in VS Code
Open VS Code.
Go to File > Open Folder... and select the project directory.

**Ensure you have the Flutter and Dart extensions installed in VS Code.**

You can install them from the Extensions view (Ctrl+Shift+X or Cmd+Shift+X).

## Step 5: Run the App
You can now run the app using VS Code:

Open the command palette (Ctrl+Shift+P or Cmd+Shift+P).
Type Flutter: Select Device and choose your preferred device (e.g., Chrome for web).
Press F5 to start debugging the app.
