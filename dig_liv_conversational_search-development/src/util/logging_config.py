import logging

def setup_logging():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.StreamHandler()  # Log to console
                        ])

# Call the setup_logging function to configure logging
setup_logging()