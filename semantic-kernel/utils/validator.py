import logging
import semantic_kernel as sk


# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
# Create a formatter
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
# Add the formatter to the console handler
console_handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)

class Validate:
    def __init__(self, to_be_validated):
        # Validate SKContext
        if  isinstance(to_be_validated, sk.SKContext):
            self.validate_SKContext(to_be_validated)
        else:
            logger.error("The variable is not of SKContext type")


    def validate_SKContext(self, to_be_validated):
        try:
            if to_be_validated.error_occurred:
                logger.error(to_be_validated.last_error_description)
            else:
                logger.info(to_be_validated.result)
        except Exception as e:
            logger.exception(str(e))
        finally:
            return to_be_validated.result