# 🎨 PosterPal

PosterPal is a simple Python script for organizing and properly renaming media artwork downloaded from sites like The Poster Database, MediUX, and more. In addition to organizing, it also optimizes/compresses the images to reduce file size. The script currently handles movies, TV shows, and episode title cards.


https://github.com/redheadjedi/posterpal/assets/67611787/b4517922-4b89-4ff8-981a-0b01392daf25



## ⚠️ Disclaimer

I am by no means a Python expert, and this script can surely be improved and made more efficient. While it works quite well in my limited testing, this was created with my minimal Python knowledge, some help from GPT, and lots of trial and error. If you have any ideas or would like to contribute/improve it in any way, please let me know!

Keep in mind that this script is currently set to overwrite any existing image files, so I recommend testing it with a test folder using your file naming scheme to make sure it's working properly. Proceed at your own risk.

## 🛠️ Setup and Configuration

1. **Install the required packages**

   Run the following command to install the necessary Python packages:

   ```bash
   pip install -r requirements.txt
   ```

2. **Configuration**

   - **Edit `config.json`**: Update this file with your specific directories and preferences.
   
     - `process`: Directory for downloads/posters. Cleared with each script run.
     - `movies`: Directory for movie storage.
     - `shows`: Directory for TV show storage.
     - `backup`: Directory for backups (if enabled).
     - `PMM_assets`: `true`/`false` for using a separate assets folder.

3. **Usage**

   Place the images, ZIPs, etc., you wish to organize into the `/process` folder and run the script. A log file will be created automatically.

## 🐳 Docker Compose Configuration

For Docker users, below is a Docker Compose configuration for setting up PosterPal. Remember to update the placeholders with your actual paths.

```yaml
version: '3.8'

services:
  posterpal:
    container_name: posterpal
    image: redheadjedi/posterpal:latest
    environment:
      PROCESS: /data/processing
      BACKUP: /data/backup
      SHOWS: /data/shows
      MOVIES: /data/movies
      ASSETS: /data/assets
      PMM_ASSETS: "false"
      CREATE_BACKUP: "true"
    volumes:
      - "/local/path/to/processing:/data/processing"
      - "/local/path/to/tv/shows:/data/shows"
      - "/local/path/to/movies:/data/movies"
      - "/local/path/to/backup:/data/backup"
      - "/local/path/to/assets:/data/assets" # Update as needed
      - "/local/path/to/logs:/var/log/posterpal" # Optional for external logging
    restart: unless-stopped
```
