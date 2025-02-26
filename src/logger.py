import logging
import coloredlogs

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

# Install coloredlogs with a custom format, level, and styles.
coloredlogs.install(
    level=logging.DEBUG,  # Set the minimum log level
    fmt='%(asctime)s [%(levelname)s] %(message)s',
    level_styles=level_styles,
    field_styles=field_styles
)

custom_logger = logging.getLogger(__name__)
logging.captureWarnings(True)