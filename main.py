import colorama
from colorama import Fore
from pytube import YouTube
import pyfiglet
from tqdm import tqdm

colorama.init(autoreset=True)

# Generate ASCII art text using pyfiglet and color it red using colorama
ascii_banner = pyfiglet.figlet_format("Youtube Downloader")
print(Fore.RED + ascii_banner)


def progress_function(stream, chunk, bytes_remaining):
    # Callback function to monitor the download progress. Updates the tqdm progress bar accordingly.
    current = (stream.filesize - bytes_remaining)
    if progress:  # Check if progress is not None
        progress.update(current - progress.n)  # Update progress bar with downloaded bytes


def download_video(url, path='downloads/'):
    # Download a video from a given YouTube URL to the specified path.
    global progress
    progress = None  # Initialize progress as None
    try:
        yt = YouTube(url)
        video = yt.streams.get_highest_resolution()

        # Initialize tqdm progress bar
        progress = tqdm(total=video.filesize, unit='B', unit_scale=True, desc="Downloading", ncols=100)

        yt.register_on_progress_callback(progress_function)

        video.download(output_path=path)
        progress.close()  # Ensure progress is closed if initialized
        print(Fore.GREEN + f'\nVideo "{yt.title}" downloaded successfully.')
    except Exception as e:
        print(Fore.RED + f'Error downloading video from URL {url}: {e}')
        if progress:  # Ensure progress is closed if initialized
            progress.close()


def main():
    # Prompt the user for a YouTube video URL and download it.

    video_url = input("Please enter a YouTube video URL: ")
    download_video(video_url)


if __name__ == "__main__":
    main()
