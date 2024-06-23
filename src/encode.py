import os
import shutil
import subprocess
import cv2
from threading import Thread
from typing import Any, AnyStr

temp_path = f"{os.getcwd()}\\temp"
Ginputpath = ""
final_render_path = ""

Gwidth: int
Gheight: int
Gfps: int
Gmode: int
Gframes: int = 1


status = "not started"
frames_progression = [0]


def get_size(filepath) -> tuple:
    size_cmd = [
        'ffprobe', '-v', 'error',
        '-show_entries', 'stream=width,height',
        '-of', 'default=nokey=1:noprint_wrappers=1',
        filepath
    ]
    size = subprocess.run(size_cmd, stdout=subprocess.PIPE, text=True)
    size = size.stdout.strip()
    width, height = size.split('\n')
    return int(width), int(height)


def get_total_frames() -> int:
    global Ginputpath, Gfps

    frames_cmd = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        '-count_frames',
        '-show_entries', 'stream=nb_read_frames',
        '-of', 'default=nokey=1:noprint_wrappers=1',
        Ginputpath
    ]

    fps_cmd = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=r_frame_rate',
        '-of', 'default=nokey=1:noprint_wrappers=1',
        Ginputpath
    ]

    frames = subprocess.run(frames_cmd, stdout=subprocess.PIPE, text=True)
    frames = int(frames.stdout.strip())

    fps = subprocess.run(fps_cmd, stdout=subprocess.PIPE, text=True)
    fps = fps.stdout.strip()
    numerator, denominator = map(int, fps.split('/'))
    fps = numerator / denominator

    return round((Gfps / fps) * frames)


def live_update(process) -> None:
    global frames_progression

    while True:
        if process.poll() is not None:
            break

        progress_text = process.stdout.readline()

        if progress_text is None:
            break

        progress_text = progress_text.decode("utf-8")

        if progress_text.startswith("frame="):
            frame = int(progress_text.partition('=')[-1])
            frames_progression[0] = frame


def create_frames(width, height, contrast: float, brightness: float, fps: int, invert: bool, input_path) -> None:
    if not os.path.exists(temp_path):
        os.mkdir(temp_path)

    if invert is True:
        invert = "negate,"
    else:
        invert = ""

    process = subprocess.Popen(["ffmpeg", "-i", f"{os.path.abspath(input_path)}",
                                "-y",
                                "-vf",
                                f"{invert}scale={width}:{height}:flags=lanczos,hue=s=0,eq=contrast={contrast}:brightness={brightness}",
                                "-r", f"{fps}",
                                "-progress", "pipe:1",
                                f"{temp_path}\\frame_%05d.png"],
                               stdout=subprocess.PIPE)
    progress_reader_thread = Thread(target=live_update,
                                    args=(process,))
    progress_reader_thread.start()
    process.wait()


def render_frame(frame: int) -> AnyStr:
    image = cv2.imread(f"temp/frame_{frame}.png")

    height, width, channels = image.shape

    rendered_frame = []

    for y in range(height):
        line = []
        for x in range(width):

            B, G, R = image[y, x]
            luminance = 0.2126 * R + 0.7152 * G + 0.0722 * B

            if luminance > 230:
                line.append("⬜")
            elif 230 > luminance > 150:
                line.append("⚪")
            elif 150 > luminance > 135:
                line.append("🤍")
            elif 135 > luminance > 65:
                line.append("🩶")
            elif 65 > luminance > 40:
                line.append("🔲")
            elif 40 > luminance > 28:
                line.append("⚫")
            else:
                line.append("⬛")
        rendered_frame.append(''.join(line))
    return '\n'.join(rendered_frame)


def render_all():
    global temp_path, final_render_path, frames_progression

    with open(f"{final_render_path}.vtd", "w+", encoding='utf-8') as file:


        file.write(add_headers())
        for i, frame in enumerate(Frames()):
            index = frame[-9:-4]
            frame = render_frame(index)
            frame = add_decorators(frame, index)

            frames_progression[0] += 1

            file.write(f"{frame}\n")
        file.write("end")
    print(temp_path)
    for i in os.listdir(temp_path):
        path = f"{temp_path}\\{i}"

        if os.path.isfile(path) or os.path.islink(path):
            os.unlink(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)


def add_decorators(frame, index):
    return f"{index}\n``\n{frame}\n``"


def add_headers():
    global Gwidth, Gheight, Gfps
    return f"{Gwidth} {Gheight} {Gfps}\n"


def Frames() -> Any:
    return os.listdir("temp/")


def encode(width: int, height: int, contrast: float, brightness: float, fps: int, invert: bool,
           input_path: str, output_path: str, filename: str):
    global final_render_path, Gwidth, Gheight, Gfps, Ginputpath, Gframes, status

    status = "initializing"
    Gwidth = width
    Gheight = height
    Gfps = fps
    Ginputpath = input_path
    Gframes = get_total_frames() * 2

    final_render_path = f"{output_path}\\{filename}"

    status = "pre-processing"
    create_frames(width, height, contrast, brightness, fps, invert, input_path)
    status = "rendering"
    render_all()
    status = "Done!"


if __name__ == '__main__':
    encode(40, 30, 1, 0, 2, False, "D:\\Downloads\\y2mate.com - 東方Bad Apple ＰＶ影絵_360p.mp4",
           "D:\\code\\Python Projects\\bad apple discord\\out", "badoople")

    # encode(1000, 500, 1.5, 0, 24, "D:\\Downloads\\y2mate.com - 東方Bad Apple ＰＶ影絵_360p.mp4",
    #        "D:\\code\\Python Projects\\bad apple discord\\out", "badoople", 0, 0)
