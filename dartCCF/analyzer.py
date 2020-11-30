from .log import setup_logger
import logging

logger = logging.getLogger('DSCA')


class Analyzer:
    def __init__(self, file_collection, logger_file):
        self.source_type = file_collection.source_type
        self.path = file_collection.path
        setup_logger(logger_file)
        logger.info("Scan {}: {}".format(self.source_type, self.path))
        self.files = file_collection.collect_files()
        logger.info("Found: %s files for analysis." % len(self.files))

    def run(self):
        logger.debug("RUN!")


class VerifyAnalyzer(Analyzer):
    def __init__(self, file_collection):
        super().__init__(file_collection, "dart_verification.log")

    def run(self):
        super().run()
        for f in self.files:
            logger.debug("Starting verification for: %s", f)


class FixAnalyzer(Analyzer):
    def __init__(self, file_collection):
        super().__init__(file_collection, "dart_fixing.log")

    def run(self):
        super().run()
        for f in self.files:
            logger.debug("Starting fix for: %s", f)
