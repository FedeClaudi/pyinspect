from PIL import Image
from pathlib import Path
import click
import pyinspect as pi
import os


pi.install_traceback()


@click.command()
@click.argument("fpath")
def get(fpath):
    print(f"Extracting gif last frame: {fpath}")
    path = Path(fpath)

    # get last image
    im = Image.open(fpath)
    im.seek(im.n_frames - 1)

    # save
    fld, name = path.parent, path.name

    newname = name.replace(".gif", ".png")

    im.save(str(fld / newname), format="png")

    print(f"Saving image at : {str(fld / newname)}")

    if "intro" not in fpath:
        os.remove(fpath)


if __name__ == "__main__":
    get()
