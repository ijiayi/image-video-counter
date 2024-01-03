import argparse
import os


def analyze_path(path):
    """Analyzes a path and returns the number of files, total size of images, and total size of videos,
    including subdirectories, using os.scandir(). Excludes folders matching "#recycle" and "@eaDir".

    Args:
        path: The path to analyze.

    Returns:
        A tuple containing the number of files, number of image files, total size of images, number of video files, and total size of videos.
    """

    num_files = 0
    num_image_files = 0
    total_image_size = 0
    num_video_files = 0
    total_video_size = 0

    with os.scandir(path) as entries:
        for entry in entries:
            if entry.is_file():
                num_files += 1
                filename, ext = os.path.splitext(entry.name)
                if ext.lower() in ('.heic', '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tif'):
                    num_image_files += 1
                    total_image_size += entry.stat().st_size
                elif ext.lower() in ('.mp4', '.mov', '.mkv'):
                    num_video_files += 1
                    total_video_size += entry.stat().st_size
            elif entry.is_dir():
                if not entry.name.startswith("#recycle") and not entry.name.startswith("@eaDir"):
                    sub_results = analyze_path(entry.path)
                    num_files += sub_results[0]
                    num_image_files += sub_results[1]
                    total_image_size += sub_results[2]
                    num_video_files += sub_results[3]
                    total_video_size += sub_results[4]

    return num_files, num_image_files, total_image_size, num_video_files, total_video_size


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze files in a path.")
    parser.add_argument("path", type=str, help="The path to analyze.")
    args = parser.parse_args()

    num_files, num_image_files, total_image_size, num_video_files, total_video_size = analyze_path(
        args.path
    )

    print(f"Number of files: {num_files}")
    print(f"Number of image files: {num_image_files}")
    print(f"Total size of images: {total_image_size / 1024 / 1024:.2f} MB")
    print(f"Number of video files: {num_video_files}")
    print(f"Total size of videos: {total_video_size / 1024 / 1024:.2f} MB")


# # Example usage
# path = "/path/to/analyze"
# num_files, total_image_size, total_video_size = analyze_path(path)

# print(f"Number of files: {num_files}")
# print(f"Total size of images: {total_image_size / 1024 / 1024:.2f} MB")
# print(f"Total size of videos: {total_video_size / 1024 / 1024:.2f} MB")
