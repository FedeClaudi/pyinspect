from pathlib import Path
from PIL import Image
from tqdm import tqdm
import subprocess


import pyinspect as pi

pi.install_traceback()


def get(fpath, start, end, repeat_last=30):
    # Open gif
    path = Path(fpath)
    im = Image.open(path)

    # check args
    if start < 0:
        start = 0
    if end > im.n_frames:
        end = im.n_frames - 1
    print(f"Trimming {fpath} to frame range {start} - {end}")

    # save frames to temp folder
    temp = path.parent / "temp"
    temp.mkdir(exist_ok=True)
    print(f"Saving frames to {temp}")
    for n, frame in tqdm(enumerate(range(start, end))):
        im.seek(frame)

        if n < 10:
            name = f"00{n}.png"
        elif n < 100:
            name = f"0{n}.png"
        else:
            name = f"{n}.png"

        im.save(temp / name)

    for i in tqdm(range(repeat_last)):
        if n < 100:
            name = f"0{n + i}.png"
        else:
            name = f"{n + i}.png"
        im.save(temp / name)

    # convert to video
    videoname = str(path).replace(".gif", ".mp4")
    subprocess.call(
        [
            "ffmpeg",
            "-i",
            f"{str(temp)}/%3d.png",
            videoname,
            "-y",
            "-framerate",
            "1",
        ]
    )

    # convert to gif
    gifname = str(path).replace(".gif", "_crop.gif")
    subprocess.call(
        [
            "ffmpeg",
            "-i",
            videoname,
            "-pix_fmt",
            "rgb24",
            "-loop",
            "0",
            gifname,
            # '-filter_complex', '[0:v] fps=1',
            "-vsync",
            "0",
            "-y",
        ]
    )


if __name__ == "__main__":
    get("media/intro.gif", 10, 88)
