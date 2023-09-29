import itertools
import random

# Test cases in spec docs
query_inputs = [
    '''create table account (
        account_number int not null,
        branch_name char(15),
        primary key(account_number)
    );''',
    'drop table account;',
    'explain account;',
    'describe account;',
    'desc account;',
    'insert into account values(9732, \'Perryridge\');',
    'delete from account where branch_name = \'Perryridge\';'
    'select * from account;',
    '''select customer_name, borrower.loan_number, amount
    from borrower, loan
    where borrower.loan_number = loan.loan_number and branch_name = 'Perryridge';''',
    'show tables;',
    'update student set id = 5 where name="susan";'
]

# CREATE TABLE, INSERT
query_inputs.extend([
    'create table person (\n'
    '   name char(10) not null,\n'
    '   address char(10) not null,\n'
    '   alias char(10),\n'
    '   age int not null,\n'
    '   height int,\n'
    '   birthdate date not null,\n'
    '   primary key (name, address),\n'
    '   foreign key (country_id) references country (id),\n'
    '   foreign key (best_friend_name, best_friend_address) references person (name, address)\n'
    ');',
    'insert into person values(\'최덕경\', "신림동", 1997-01-17);',
    'insert into person (name, address, birth) values(\'최덕경\', "신림동", 1997-01-17);'
])

comparison_predicates = []
for comb in itertools.product(['a', 't.a', '3', '\'3\'', '"3"', '1997-01-17'], ['=', '!='],
                              ['a', 't.a', '3', '\'3\'', '"3"', '1997-01-17']):
    comparison_predicates.append(f'{comb[0]} {comb[1]} {comb[2]}')

null_predicates = []
for comb in itertools.product(['a', 't.a'], ['is', 'is not']):
    null_predicates.append(f'{comb[0]} {comb[1]} null')

boolean_factors = comparison_predicates + null_predicates
boolean_factors += list(map(lambda x: 'not ' + x, boolean_factors))

boolean_factors_sample = random.choices(boolean_factors, k=50)
boolean_factor_sample_group = [
    boolean_factors_sample[4 * i:4 * (i + 1)]
    for i in range(len(boolean_factors_sample) // 4)
]

conditions = []
for comb in itertools.product(['and', 'or'], ['and', 'or'], ['and', 'or']):
    for group in boolean_factor_sample_group:
        conditions.append(f'{group[0]} {comb[0]} {group[1]} {comb[1]} {group[2]} {comb[2]} {group[3]}')

# DELETE
for condition in conditions:
    query_inputs.append(f'delete from students where {condition};')

# UPDATE
for condition in conditions:
    for v in ['3', '\'3\'', '"3"', '1997-01-17']:
        query_inputs.append(f'update students set a = {v} where {condition};')
