import os
import shutil
import zipfile
import re
import json
import sys
from datetime import datetime
from fuzzywuzzy import process
import logging
from PIL import Image

# Set up logging
log_filename = 'log.txt'
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


def load_config(config_filename):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(script_dir, config_filename)
    if os.path.isfile(config_path):
        with open(config_path, 'r') as config_file:
            return json.load(config_file)
    else:
       config = {
            "process": os.environ["PROCESS"],
            "backup": os.environ["BACKUP"],
            "movies": os.environ["MOVIES"],
            "shows": os.environ["SHOWS"],
            "assets": os.environ["ASSETS"],
            "pmm_assets": os.environ["PMM_ASSETS"].lower() == "true",
            "create_backup": os.environ["CREATE_BACKUP"].lower() == "true"
        }
       return config
        

def scan_directories(base_dir):
    return {os.path.normcase(name) for name in os.listdir(base_dir)}

def determine_category(name, shows_set, movies_set):
    normalized_name = os.path.normcase(name)
    if normalized_name in shows_set:
        return 'show'
    elif normalized_name in movies_set:
        return 'movie'
    return None

def find_closest_directory_name(target, directory_set):
    target = target.lower()
    closest, score = process.extractOne(target, directory_set, score_cutoff=90)
    return closest if closest and score > 85 else None

def process_file_name(file_name, shows_dir, movies_dir, shows_set, movies_set):
    season_folder = ""
    season_episode_pattern = re.compile(r'(.*?)(?: -)? (S\d+ E\d+).*(\..+)$', re.IGNORECASE)
    season_pattern = re.compile(r'(.*?)(?: -)? Season (\d+).*(\..+)$', re.IGNORECASE)
    poster_pattern = re.compile(r'(.*?)\s*\((\d{4})\)\.(\w+)$', re.IGNORECASE)
    backdrop_pattern = re.compile(r'(.*?)\s*\((\d{4})\) backdrop\.(\w+)$', re.IGNORECASE)

    se_match = season_episode_pattern.match(file_name)
    s_match = season_pattern.match(file_name)
    p_match = poster_pattern.match(file_name)
    b_match = backdrop_pattern.match(file_name)

    if se_match or s_match or p_match or b_match:
        name = (se_match or s_match or p_match or b_match).group().strip()
        category = determine_category(name, shows_set, movies_set)
        
        if category is None:
            directory_name = find_closest_directory_name(name, shows_set.union(movies_set))
            if directory_name:
                category = 'show' if directory_name in shows_set else 'movie'
            else:
                logging.warning(f"Skipping '{file_name}': No matching show or movie found and no close match for '{name}'.")
                return None, False

        if b_match:
            new_file_name = "background.jpg"
        elif se_match:
            season_episode, extension = se_match.groups()[1], se_match.groups()[2]
            season, episode = season_episode.split()[0][1:], season_episode.split()[1][1:]
            if season == "0":
                season_folder = "Specials"
                new_file_name = "specials.jpg"
            else:
                season_folder = f"Season {int(season)}"
                new_file_name = f"S{int(season):02d}E{int(episode):02d}{extension}"
        elif s_match:
            season, extension = s_match.groups()[1], s_match.groups()[2]
            if season == "0":
                season_folder = "Specials"
                new_file_name = "specials.jpg"
            else:
                season_folder = f"Season {int(season)}"
                new_file_name = f"season{int(season):02d}{extension}"
        elif p_match:
            new_file_name = "poster.jpg"

        if category == 'show':
            show_directory = directory_name if 'directory_name' in locals() else name
            target_dir = os.path.join(shows_dir, show_directory, season_folder)
        elif category == 'movie':
            movie_directory = directory_name if 'directory_name' in locals() else name
            target_dir = os.path.join(movies_dir, movie_directory)
    else:
        logging.warning(f"Skipping '{file_name}': File does not match expected patterns.")
        return None, False

    os.makedirs(target_dir, exist_ok=True)
    full_new_path = os.path.join(target_dir, new_file_name)
    logging.info(f"Preparing to move '{file_name}' to '{full_new_path}'.")
    return full_new_path, True

def compress_and_convert_images(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpeg', '.bmp', '.gif', '.tiff', '.jpg')):
                original_path = os.path.join(root, file)
                new_file = os.path.splitext(file)[0] + '.jpg'
                new_path = os.path.join(root, new_file)
                
                try:
                    with Image.open(original_path) as img:
                        if img.mode in ('RGBA', 'LA', 'P'):
                            img = img.convert("RGB")
                        img.save(new_path, 'JPEG', quality=85, optimize=True)
                        
                    if new_file.lower() != file.lower():
                        os.remove(original_path)
                    logging.info(f"Compressed and converted '{file}' to JPEG.")
                except Exception as e:
                    logging.error(f"Failed to compress '{file}': {e}")

def backup_files(source_dir, backup_dir):
    for item in os.listdir(source_dir):
        item_path = os.path.join(source_dir, item)
        backup_path = os.path.join(backup_dir, item)

        if os.path.exists(backup_path):
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            base_name, extension = os.path.splitext(item)
            backup_item = f"{base_name}_{timestamp}{extension}"
            backup_path = os.path.join(backup_dir, backup_item)

        shutil.copy2(item_path, backup_path)
        logging.info(f"Backed up '{item}' to '{backup_path}'.")

def unzip_files(source_dir):
    for item in os.listdir(source_dir):
        item_path = os.path.join(source_dir, item)

        if item.endswith('.zip'):
            with zipfile.ZipFile(item_path, 'r') as zip_ref:
                zip_ref.extractall(source_dir)
            os.remove(item_path)
            logging.info(f"Unzipped '{item}'.")

def clear_directory(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            os.remove(file_path)
        for name in dirs:
            dir_path = os.path.join(root, name)
            os.rmdir(dir_path)
    logging.info(f"Cleared {directory}.")

def rename_episode_images(shows_dir):
    video_extensions = {'.mkv', '.mp4', '.avi', '.mov'}
    for root, dirs, files in os.walk(shows_dir):
        video_files = {file for file in files if os.path.splitext(file)[1].lower() in video_extensions}
        image_files = {file for file in files if file.lower().endswith('.jpg')}
        
        for image_file in image_files:
            image_base = os.path.splitext(image_file)[0]
            for video_file in video_files:
                video_base = os.path.splitext(video_file)[0]
                if image_base.lower().startswith('s') and image_base.lower() in video_base.lower():
                    new_image_name = video_base + '.jpg'
                    os.rename(os.path.join(root, image_file), os.path.join(root, new_image_name))
                    logging.info(f"Renamed '{image_file}' to match video file '{video_file}'.")

def process_files(config):
    logging.info("Starting file processing.")
    process_dir = config['process']
    backup_dir = config['backup']
    shows_dir = config['shows']
    movies_dir = config['movies']
    assets_dir = config['assets']
    assets_bool = config['pmm_assets']
    backup_bool = config['create_backup']

    if backup_bool == True:
        backup_files(process_dir, backup_dir)
    
    unzip_files(process_dir)

    if assets_bool == False:
        shows_set = scan_directories(shows_dir)
        movies_set = scan_directories(movies_dir)
        compress_and_convert_images(process_dir)
        for root, _, files in os.walk(process_dir):
            for file in files:
                if file.startswith('._') or file == '.DS_Store':
                    continue
                
                try:
                    full_new_path, is_episode_image = process_file_name(file, shows_dir, movies_dir, shows_set, movies_set)
                    if full_new_path:
                        shutil.move(os.path.join(root, file), full_new_path)
                except TypeError:
                    continue

        clear_directory(process_dir)
        rename_episode_images(shows_dir)
        logging.info("Finished processing all files.")
    else:
        assets_set = scan_directories(assets_dir)
        compress_and_convert_images(process_dir)

        for root, _, files in os.walk(process_dir):
            for file in files:
                if file.startswith('._') or file == '.DS_Store':
                    continue

                try:
                    full_new_path, is_episode_image = process_file_name(file, assets_dir, assets_dir, assets_set, assets_set)
                    if full_new_path:
                        shutil.move(os.path.join(root, file), full_new_path)
                except TypeError:
                    continue

        clear_directory(process_dir)
        rename_episode_images(assets_set)
        logging.info("Finished processing all files.")

if __name__ == "__main__":
    try:
        config = load_config("config.json")
        process_files(config)
        logging.info("Script completed successfully.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
