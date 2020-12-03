from .log import setup_logger
import logging
import re

logger = logging.getLogger('DSCA')


class Analyzer:
    def __init__(self, file_collection, logger_file, log_tag):
        self.source_type = file_collection.source_type
        self.path = file_collection.path
        self.log_tag = log_tag
        setup_logger(logger_file)
        logger.debug("Scan {}: {}".format(self.source_type, self.path))
        self.files = file_collection.collect_files()
        logger.debug("Found: %s files for analysis." % len(self.files))

    def run(self):
        for file in self.files:
            logger.debug(f'Starting {self.log_tag} for: {file}')
            verify_file(file)
        pass

    pass


class VerifyAnalyzer(Analyzer):
    def __init__(self, file_collection):
        super().__init__(file_collection, "dart_verification.log", "verification")
        pass

    pass


class FixAnalyzer(Analyzer):
    def __init__(self, file_collection):
        super().__init__(file_collection, "dart_fixing.log", "fixing")
        pass

    pass


def verify_file(file):
    verify_file_names(file)
    with open(file) as f:
        lines = f.readlines()
        for num, code_line in enumerate(lines, start=1):
            verify_line_length(file, num, code_line)
            verify_package_imports(file, num, code_line)
            verify_camel_case_types(file, num, code_line)
            verify_camel_case_extensions(file, num, code_line)
            verify_library_names(file, num, code_line)
            verify_library_prefixes(file, num, code_line)
            verify_constant_identifier_names(file, num, code_line)
            verify_curly_braces_in_flow_control_structures(file, num, code_line)
            verify_slash_for_doc_comments(file, num, code_line)
            verify_is_empty_collection(file, num, code_line)
            verify_is_not_empty_iterable(file, num, code_line)


def verify_line_length(file, num, code_line):
    if len(code_line) > 80:
        logger.info(f'{file}: Line:{num} - lines_longer_than_80_chars: Avoid lines longer than 80 characters.')


def verify_package_imports(file, num, code_line):
    match = re.search(r'import\s+\'([^\']*)\'', code_line)
    if match:
        import_name = match.group(1)
        if import_name.find(":") > 0:
            logger.info(f'{file}: Line:{num} - always_use_package_imports: DO avoid relative imports for '
                        f'files in lib/.')


def verify_camel_case_types(file, num, code_line):
    match = re.search(r'(class|typedef)\s+(\w+)(<[^>]*>)?\s*({|extends)', code_line)
    if match:
        class_name = match.group(2)
        if not is_camel_case(class_name):
            logger.info(f'{file}: Line:{num} - camel_case_types: DO name types using UpperCamelCase.')


def verify_camel_case_extensions(file, num, code_line):
    match = re.search(r'extension\s+(\w+)(<[^>]*>)?\s+on', code_line)
    if match:
        extension_name = match.group(1)
        if not is_camel_case(extension_name):
            logger.info(f'{file}: Line:{num} - camel_case_extensions: DO name extensions using UpperCamelCase.')


def verify_library_names(file, num, code_line):
    match = re.search(r'library\s+(\w+)\s*;', code_line)
    if match:
        library_name = match.group(1)
        if not is_snake_case(library_name):
            logger.info(f'{file}: Line:{num} - library_names: DO name libraries using lowercase_with_underscores.')


def verify_file_names(file):
    match = re.search(r'(\w+).dart$', file)
    if match:
        file_name = match.group(1)
        if not is_snake_case_full(file_name):
            logger.info(f'{file}: file_names: DO name source files using lowercase_with_underscores.')


def verify_library_prefixes(file, num, code_line):
    match = re.search(r'import\s+\'[^\']*\'\s+as\s+(\w+)\s*;', code_line)
    if match:
        library_prefix = match.group(1)
        if not is_snake_case(library_prefix):
            logger.info(f'{file}: Line:{num} - library_prefixes: DO use lowercase_with_underscores when specifying a '
                        f'library prefix.')


def verify_constant_identifier_names(file, num, code_line):
    match = re.search(r'(const|final)\s+(\w+)\s*=', code_line)
    if match:
        constant_name = match.group(1)
        if not is_lower_camel_case(constant_name):
            logger.info(
                f'{file}: Line:{num} - constant_identifier_names: PREFER using lowerCamelCase for constant names')


def verify_curly_braces_in_flow_control_structures(file, num, code_line):
    match = re.search(r'if \([^)]*\)\s+(.*)', code_line)
    if match:
        if not match.group(1).startswith("{"):
            check_curly_brace(file, num, match.group(1))
    else:
        match = re.search(r'else\s+(.*)', code_line)
        if match:
            check_curly_brace(file, num, match.group(1))


def check_curly_brace(file, num, line):
    if not line.startswith("{"):
        logger.info(
            f'{file}: Line:{num} - curly_braces_in_flow_control_structures: DO use curly braces for all flow control '
            f'structures.')


def verify_slash_for_doc_comments(file, num, code_line):
    match = re.search(r'/\*\*', code_line)
    if match:
        logger.info(f'{file}: Line:{num} - slash_for_doc_comments: PREFER using /// for doc comments.')


def verify_is_empty_collection(file, num, code_line):
    match = re.search(r'\.length\s*(==|!=)', code_line)
    if match:
        logger.info(f'{file}: Line:{num} - prefer_is_empty: DON\'T use length to see if a collection is empty.')


def verify_is_not_empty_iterable(file, num, code_line):
    match = re.search(r'if\s*\((.*)\)', code_line)
    if match:
        for statement in re.split(r'(&&|\|\|)', match.group(1)):
            if re.search(r'^\s*\!.*isEmpty\s*$', statement):
                logger.info(
                    f'{file}: Line:{num} - prefer_is_not_empty: PREFER x.isNotEmpty to !x.isEmpty for Iterable and '
                    f'Map instances.')


def is_camel_case(word):
    if re.match(r'^[A-Z]+[a-zA-Z0-9]*$', word):
        return True
    else:
        return False


def is_lower_camel_case(word):
    if re.match(r'^[a-z]+[a-zA-Z0-9]*$', word):
        return True
    else:
        return False


def is_snake_case(word):
    if re.match(r'^[a-z_]+[a-z0-9_]*$', word):
        return True
    else:
        return False


def is_snake_case_full(word):
    if re.match(r'^[a-z0-9_]+$', word):
        return True
    else:
        return False
