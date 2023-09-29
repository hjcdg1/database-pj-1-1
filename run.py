import atexit
import sys

from lark import Lark, Transformer, exceptions

PROMPT_TEXT = 'DB_2016-10399'


class SQLExecutor(Transformer):
    def execute(self, tree):
        """
        Rename `transform` method for improving readabilit
        """

        self.transform(tree)

    def print_success_msg(self, query_type):
        """
        Print success message based on the query's type
        """

        print(f'{PROMPT_TEXT}> \'{query_type}\' requested')

    def create_table_query(self, items):
        self.print_success_msg('CREATE TABLE')

    def drop_table_query(self, items):
        self.print_success_msg('DROP TABLE')

    def explain_query(self, items):
        self.print_success_msg('EXPLAIN')

    def describe_query(self, items):
        self.print_success_msg('DESCRIBE')

    def desc_query(self, items):
        self.print_success_msg('DESC')

    def insert_query(self, items):
        self.print_success_msg('INSERT')

    def delete_query(self, items):
        self.print_success_msg('DELETE')

    def select_query(self, items):
        self.print_success_msg('SELECT')

    def show_tables_query(self, items):
        self.print_success_msg('SHOW TABLES')

    def update_query(self, items):
        self.print_success_msg('UPDATE')

    def exit_query(self, items):
        # Skip the remaining queries and terminate this process
        exit(0)


def read_query_input():
    # Read a query input from user, which can be multi-lines or multi-queries
    query_input_lines = []
    while True:
        query_input_line = input().strip()
        query_input_lines.append(query_input_line)

        # Stop reading lines for current input, when encountering semicolon character at the end of the line
        if query_input_line.endswith(';'):
            break

    # Concatenate each line of the input with whitespace character, resulting in a cleaned query input
    return ' '.join(query_input_lines)


def parse_query_input(parser, executor, query_input):
    # Split the query input into multiple queries, where each query ends with semicolon character
    query_list = map(lambda query: query + ';', query_input[:-1].split(';'))

    # For each query
    for query in query_list:
        # Parse the query, and make a tree representing the parsed result as hierarchical nodes
        try:
            tree = parser.parse(query)

        # When parsing failed, print `Syntax error` and skip the remaining queries
        except exceptions.UnexpectedInput:
            print(f'{PROMPT_TEXT}> Syntax error')
            break

        # When parsing is successful, print success message based on the query's type
        # But if the query's type is `EXIT`, skip the remaining queries and terminate this process (`exit_query` method)
        executor.execute(tree)


def cleanup():
    # Reclaim memory resources before terminating this process
    grammar.close()


# Register a cleanup function, which will be called when this process is terminated
atexit.register(cleanup)

# Instantiate a SQL parser from a lark file, which defines the grammar for parsing SQL
grammar = open('grammar.lark')
parser = Lark(grammar.read(), start='command', lexer='basic')

# Instantiate a SQL executor for handling each type of query
executor = SQLExecutor()

# Test mode (Use inputs constructed in `test_cases.py`)
if len(sys.argv) > 1 and sys.argv[1] == '--test':
    from src.test_cases import query_inputs

    for query_input in query_inputs:
        parse_query_input(parser, executor, query_input)

# Default mode
else:
    # Keep reading query inputs from user, before encountering `EXIT` query
    while True:
        # Prompt for a query input
        print(f'{PROMPT_TEXT}>', end=' ')

        # Read a query input from user
        query_input = read_query_input()

        # Parse the query input, and execute the queries
        parse_query_input(parser, executor, query_input)
