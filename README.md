# PosterPal

PosterPal is a simple Python script for organizing and properly renaming media artwork downloaded from sites like The Poster Database, MediUX, and more. In addition to organizing, it also optimizes/compresses the images to reduce file size. The script currently handles movies, TV shows, and episode title cards.

## ⚠️ Disclaimer

I am by no means a Python expert, and this script can surely be improved and made more efficient. While it works quite well in my limited testing, this was created with my minimal Python knowledge, some help from GPT, and lots of trial and error. If you have any ideas or would like to contribute/improve it in any way, please let me know!

Keep in mind that this script is currently set to overwrite any existing image files, so I recommend testing it with a test folder using your file naming scheme to make sure it's working properly. Proceed at your own risk.

## Setup and Configuration

### 1. Install the required packages

```bash
pip install -r requirements.txt
```

### 2. Edit the `config.json` file with your directories and preferences

#### Main Directories

- `process`: This is where you will place all of your downloads/posters from TPDb, MediUX, etc. This folder will be cleared every time you run the script.
- `movies`: This should be where you store all of your movies. Ideally, the folders should contain the title and year.
- `shows`: This should be where you store all of your TV shows.

#### Backup (optional)

- `create_backup`: `true` or `false`. Used for toggling backups.
- `backup`: This is where it will place backups of everything you drop into the `process` folder.

#### Plex Meta Manager Assets (optional)

- `PMM_assets`: `true` or `false`. Set to `true` if you prefer to use a separate "assets" folder for your artwork instead of storing it alongside the media itself. Please keep in mind that the script does not currently create directories, so they must already exist before running the script.
- `assets`: This should be your PMM assets folder.

### 3. Drop the images, ZIPs, etc., you want to organize into the `/process` folder, and run the script! A log file will be created automatically.

**Note:** This script uses a fuzzy search to identify matches. This can be adjusted in the script itself.
