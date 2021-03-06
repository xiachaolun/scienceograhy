import os

db_address = 'USE YOUR OWN'
db_port = 27017

# db
db_name = 'scienceography'

# collections
main_paper_list = 'main_paper_list' # from all domain year = 2000, citation >= 100
all_paper_list = 'all_paper_list' # covers all domains
citing_paper = 'citing_paper'
main_paper_with_context = 'main_paper_with_context' # with >= 100 citations published between 1998-2003
main_paper_with_citation = 'main_paper_with_citation'
main_paper_with_reference = 'main_paper_with_reference'
main_paper_with_abstract = 'main_paper_with_abstract'
other_paper_with_abstract = 'other_paper_with_abstract'
main_author_list = 'main_author_list'
all_venue_with_info = 'all_venue_with_info'
main_paper_with_all_info = 'main_paper_with_all_info'


redis_server = 'tall2'

test_data = 'test_data'

time_out = 1000000