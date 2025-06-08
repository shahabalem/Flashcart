from datetime import timedelta

# max file sizes
MAX_AVATAR_FILE_SIZE = 4194305  # 4 mb
MAX_COVER_FILE_SIZE = 10485761  # 10 mb
MAX_POST_FILE_SIZE = 52428801  # 50 mb
MAX_BLOG_FILE_SIZE = 52428801  # 50 mb
MAX_EXHIBITION_FILE_SIZE = 10485761  # 10 mb
DATA_UPLOAD_MAX_MEMORY_SIZE = (
    52428801  # 50 mb (this will use in middleware with django by default)
)


# Deactivate days
DEACTIVATE_DAYS = 7

# Email Change Date
EMAIL_CHANGE_PERIOD = timedelta(days=30)


# Count
DEFAULT_COUNT_VALUE = 1
MINIMUM_COUNT_VALUE = 1
MAXIMUM_COUNT_VALUE = 100
MAXIMUM_COUNT_RESTRICT_VALUE = 20


# Default page size
PAGINATE_PAGE_SIZE = 12

# Exception variable
DEFAULT_STATUS_KEY = 'status'
DEFAULT_DETAIL_KEY = "detail"
FORBIDDEN_MESSAGE = {
    DEFAULT_DETAIL_KEY: "You have not permission to perform this action"
}


# Storage variable
STORAGE_URL = "https://content.flashcard.com"
MEDIA_URL = "https://content.flashcard.com/media/"
AWS_S3_ENDPOINT_URL = "https://flashcard-storage.nyc3.digitaloceanspaces.com"
