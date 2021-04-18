import io, os
from pydub import AudioSegment

def bytes_len(BytesIO_obj):
    BytesIO_obj.seek(0, os.SEEK_END)
    len = BytesIO_obj.tell()
    BytesIO_obj.seek(0)
    return len

def process_audio(wav_bytes):
    y = AudioSegment.from_file(io.BytesIO(wav_bytes), format="wav")
    y = y.set_frame_rate(16000).set_channels(1)

    z = io.BytesIO()
    y.export(z, format = 'wav')

    return z
