# ⚠️ No Longer Maintained - Use AssetAssistant

This project is no longer maintained and has been archived. I recommend using **AssetAssistant** by my good friend **mikenobbs**, which offers a superior experience. You can find it [here](https://github.com/mikenobbs/Asset-Assistant).

# 🎨 PosterPal

PosterPal is a simple Python script for organizing and properly renaming media artwork downloaded from sites like The Poster Database, MediUX, and more. In addition to organizing, it also optimizes/compresses the images to reduce file size. The script currently handles movies, TV shows, and episode title cards.

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
