import logging
import warnings
import coloredlogs
import sys
import os

# Define custom color styles for each log level
level_styles = {
    'debug': {'color': 'blue'},
    'info': {'color': 'green'},
    'warning': {'color': 'yellow'},
    'error': {'color': 'red'},
    'critical': {'color': 'red', 'bold': True},
}

# Optionally, you can also customize field styles (e.g., timestamp)
field_styles = {
    'asctime': {'color': 'cyan'},
    'levelname': {'bold': True},
}

# Create a formatter for file logging
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

# Create a custom logger
custom_logger = logging.getLogger("book_recommendation_system")
custom_logger.setLevel(logging.DEBUG)
custom_logger.propagate = True  # changed from False

# Ensure logs directory exists
logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
os.makedirs(logs_dir, exist_ok=True)

# Create handlers
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(os.path.join(logs_dir, "app.log"))
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Add handlers to logger if they don't exist already
if not custom_logger.handlers:
    custom_logger.addHandler(console_handler)
    custom_logger.addHandler(file_handler)

# Install coloredlogs for the console handler
coloredlogs.install(
    level=logging.DEBUG,
    logger=custom_logger,
    fmt='%(asctime)s [%(levelname)s] %(message)s',
    level_styles=level_styles,
    field_styles=field_styles,
    isatty=True,  # Force colored output
    stream=sys.stdout
)

# Configure third-party loggers
for logger_name, level in [
    ("transformers", logging.ERROR),
    ("huggingface_hub", logging.ERROR),
    ("httpx", logging.WARNING),
    ("httpcore", logging.WARNING),
    ("openai", logging.WARNING),
    ("uvicorn", logging.INFO),
    ("apscheduler", logging.INFO),
    ("alembic", logging.INFO),
]:
    third_party_logger = logging.getLogger(logger_name)
    third_party_logger.setLevel(level)
    # Optionally, you can make these loggers use your handlers
    # for handler in custom_logger.handlers:
    #     third_party_logger.addHandler(handler)

# Suppress warnings
warnings.filterwarnings("ignore")
logging.captureWarnings(True)

# Function to get the logger from anywhere in the application
def get_logger():
    return custom_logger