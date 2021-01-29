'''
Author: Tianyi Lu
Description: Postgresql command-line interface
Date: 2021-01-29 18:05:08
LastEditors: Tianyi Lu
LastEditTime: 2021-01-30 00:40:38
'''
import psycopg2
import argparse

try:
    import config
except Exception as e:
    print(e)
    print("Please create a config.py in the current directory!")
    exit()


class Olympics(object):
    def __init__(self):
        self.__connection = self.__get_connection(config.database, 
                                   config.username, 
                                   config.password)

        self.__cursor = self.__get_cursor()

    def __del__(self):
        self.__connection.close() # Close the connection to psql when function ends
        
    def __get_connection(self, database, user, password):
        try:
            connection = psycopg2.connect(database=database, 
                                          user=user, 
                                          password=password)
        except Exception as e:
            print(e)
            exit()

        return connection

    def __get_cursor(self):
        try:
            cursor = self.__connection.cursor()
        except Exception as e:
            print(e)
            exit()

        return cursor

    def get_athletes(self, nocs=[], names=[]):
        """
        Get a list of athletes by specific noc and name.
        :param nocs: a list of nocs to get athletes from
        :param names: a list of name strings to search athletes' names
        :return: a list of tuples containing athlete information
        """
        query_head = '''SELECT DISTINCT athletes.full_name, nocs.noc_name
                        FROM athletes, nocs, athletes_nocs
                        WHERE athletes.id = athletes_nocs.athlete_id
                        AND nocs.id = athletes_nocs.noc_id'''
                 
        query_tail = '''ORDER BY athletes.full_name;'''

        final_result_set = set()

        if nocs:
            noc_result_set = set()
            for noc in nocs:
                query_full = query_head + \
                             "\nAND nocs.noc_name like '%{}%'".format(noc.upper())\
                             + query_tail
                self.__cursor.execute(query_full)
                for row in self.__cursor:
                    noc_result_set.add(row)
            final_result_set = noc_result_set

        if names:
            name_result_set = set()
            for name in names:
                query_full = query_head + \
                             "\nAND lower(athletes.full_name) like '%{}%'".format(name.lower())\
                             + query_tail
                self.__cursor.execute(query_full)
                for row in self.__cursor:
                    name_result_set.add(row)
            
            if final_result_set:
                final_result_set &= name_result_set 
            else:
                final_result_set = name_result_set 
        
        final_result_list = sorted(list(final_result_set), key=lambda x: x[0])
        return final_result_list

    def get_nocs_with_medals(self, medal_type='gold'):
        """
        Get a list of nocs ordered by the number of medals they won.
        :param medal_type: can be gold, silver or bronze 
        :return: a list of tuples containing ordered noc information
        """
        query = '''SELECT nocs.noc_name, COUNT(medals.medal)
                   FROM nocs, athletes, medals, athletes_nocs
                   WHERE athletes.id = medals.athlete_id
                   AND athletes.id = athletes_nocs.athlete_id
                   AND nocs.id = athletes_nocs.noc_id
                   AND lower(medals.medal) like '%{}%'
                   GROUP BY nocs.noc_name
                   ORDER BY COUNT(medals.medal) DESC;'''.format(medal_type.lower())
                                                            
        self.__cursor.execute(query)

        return [row for row in self.__cursor]

    def get_best_noc_in_year(self, year):
        """
        Get the noc with the most number of gold in a given year
        :param year:
        :return: a string containing information for the best noc
        """
        query = '''SELECT nocs.noc_name, COUNT(medals.medal)
                   FROM nocs, athletes, medals, athletes_nocs, games
                   WHERE athletes.id = medals.athlete_id
                   AND games.id = medals.game_id
                   AND athletes.id = athletes_nocs.athlete_id
                   AND nocs.id = athletes_nocs.noc_id
                   AND lower(medals.medal) = 'gold'
                   AND games.game_year = '{}'
                   GROUP BY nocs.noc_name
                   ORDER BY COUNT(medals.medal) DESC;'''.format(year)
        
        self.__cursor.execute(query)
        return next(self.__cursor)
    
def get_arguments():
    """
    Get argument from command line
    :return: args object
    """
    parser = argparse.ArgumentParser(prog="python3 olympics.py",
                                     description="Search for data in olympics database",
                                     epilog="Run -h for each positional arguments to see more details.")

    subparsers = parser.add_subparsers(help='sub-command help', dest='subcommand')

    parser_athlete = subparsers.add_parser('athlete', 
                                           help="print athletes based on different options")

    parser_athlete.add_argument('-n', '--nocs', type=str, nargs='+',
                                help="print all athletes in the given nocs in the arguments")

    parser_athlete.add_argument('-a', '--name', type=str, nargs='+',
                                help="print all athletes whose names contains the arguments")

    parser_noc = subparsers.add_parser('noc', 
                                       help="print nocs based on counts of medals")
    
    parser_noc.add_argument('-m', '--medal', type=str, nargs='?', choices=['gold', 'silver', 'bronze'],
                            help="order nocs based on the type of medal in the argument")

    parser_game = subparsers.add_parser('game',
                                         help="print the country winning the most number of gold in a give year")
    
    parser_game.add_argument('-y', '--year', type=str, nargs='?',
                            help="print the country winning the most number of gold in a give year")
        
    args = parser.parse_args()

    return args

def print_athlete_result(athlete_list):
    print("Name\t\t\tNOC")
    for row in athlete_list:
        print('\t\t\t'.join(row))
    
def print_noc_medal_result(noc_list):
    print("NOC\t\t\tMedals")
    for row in noc_list:
        print('\t\t\t'.join([row[0], str(row[1])]))

def print_best_noc(best_noc):
    print("The NOC with the most number of gold is:")
    print('\t'.join([best_noc[0], str(best_noc[1])]))

def main():
    olympics = Olympics()
    args = get_arguments()

    if args.subcommand == 'athlete':
        athlete_list = olympics.get_athletes(nocs=args.nocs,
                                             names=args.name)
        print_athlete_result(athlete_list)

    elif args.subcommand == 'noc':
        noc_list = olympics.get_nocs_with_medals(medal_type=args.medal or 'gold')
        print_noc_medal_result(noc_list)

    elif args.subcommand == 'game':
        best_noc = olympics.get_best_noc_in_year(year=args.year)        
        print_best_noc(best_noc)

if __name__ == "__main__":
    main()