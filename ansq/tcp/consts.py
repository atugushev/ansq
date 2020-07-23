NL = b'\n'
DATA_SIZE = 4
FRAME_SIZE = 4
HEADER_SIZE = DATA_SIZE + FRAME_SIZE

TIMESTAMP_SIZE = 8
ATTEMPTS_SIZE = 2
MSG_ID_SIZE = 16
MSG_HEADER = TIMESTAMP_SIZE + ATTEMPTS_SIZE + MSG_ID_SIZE
MAX_CHUNK_SIZE = 4096
