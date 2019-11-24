import binascii
from datetime import datetime
import exifread
import av
import os
import plac
from shutil import move, copy


FIELDS = [
    'EXIF DateTimeOriginal',
    'EXIF DateTimeDigitized',
    'Image DateTime'
]

FORMATS = [
    '%Y-%m-%d %H:%M:%S',
    '%Y:%m:%d %H:%M:%S'
]

EXTENSIONS = [
    '.jpg',
    '.jpeg',
    '.png',
    '.PNG',
    '.JPG',
    '.JPEG',
    '.mp4'
]


def iterfiles(cwd):
    for f in os.listdir(cwd):
        for e in EXTENSIONS:
            if f.endswith(e):
                yield f


def get_timestamp(f, name):
    ext = get_ext(name)
    if ext == 'jpg' or ext == 'png':
        return get_exif_timestamp(f, name)
    if ext == 'mp4':
        return get_mp4_timestamp(f, name)
    print("Invalid extension {}".format(ext))
    return None


def get_exif_timestamp(f, name):
    tags = exifread.process_file(f)
    f.seek(0)

    for field in FIELDS:
        if field in tags and tags[field] is not None:
            v = tags[field].values.replace('24:', '00:')
            for fmt in FORMATS:
                try:
                    ts = datetime.strptime(v, fmt)
                    return ts
                except ValueError:
                    pass

    # fall back to file modification time or creation time, whichever is
    # earlier - this deals with an issue observed with copied files
    mtime = datetime.utcfromtimestamp(os.path.getmtime(name))
    ctime = datetime.utcfromtimestamp(os.path.getctime(name))
    if ctime < mtime:
        return ctime
    return mtime


def get_mp4_timestamp(f, name):
    container = av.open(name)
    raw = container.metadata['creation_time'].split('.')[0]
    return datetime.strptime(raw, "%Y-%m-%dT%H:%M:%S")


def get_hash(f):
    buf = f.read()
    f.seek(0)
    return binascii.crc32(buf) & 0xFFFFFFFF


def get_ext(filename):
    ext = filename.split('.')[-1].lower()
    if filename.lower().endswith('.jpeg'):
        ext = '.jpg'
    return ext


def create_filename(filename):
    with open(filename, 'rb') as f:
        ext = get_ext(filename)

        ts = get_timestamp(f, filename)
        if ts is None:
            return None

        h = get_hash(f)

        return "{y:02d}{m:02d}{d:02d}_{h:02d}{M:02d}{s:02d}_{H:08x}.{e}" \
            .format(y=ts.year,
                    m=ts.month,
                    d=ts.day,
                    h=ts.hour,
                    M=ts.minute,
                    s=ts.second,
                    H=h,
                    e=ext)


def main(source: ("source", "positional"),
         dest: ("dest", "positional"),
         dry_run: ("dry-run", "flag", "n"),
         mv: ("move", "flag", "m")):
    for filename in iterfiles(source):
        filename = os.path.join(source, filename)
        new_filename = create_filename(filename)
        if new_filename is None:
            print("{dry}skipping {filename}".format(
                filename=filename,
                dry="[dry-run] " if dry_run else ""))
            continue

        year = new_filename[0:4]
        if not os.path.isdir(os.path.join(dest, year)):
            os.makedirs(os.path.join(dest, year))

        new_filename = os.path.join(dest, year, new_filename)
        if os.path.isfile(new_filename):
            print("{dry}{filename} already exists".format(
                dry="[dry-run] " if dry_run else "",
                filename=new_filename))
            continue

        print("{dry}{mode} {old} => {new}".format(
                dry="[dry-run] " if dry_run else "",
                mode="move" if mv else "copy",
                old=filename,
                new=filename))

        if dry_run:
            continue
        if mv:
            move(filename, new_filename)
        else:
            copy(filename, new_filename)


def _main():
    plac.call(main)


if __name__ == '__main__':
    _main()
