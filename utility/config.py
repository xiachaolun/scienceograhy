import os

db_address = 'grande.rutgers.edu'
db_port = 27017

# db
db_name = 'scienceography'

# collections
other_paper_list = 'other_paper_meta_data'
paper_list = 'paper_meta_data'
citing_paper = 'citing_paper'
main_paper_with_context = 'main_paper_with_context' # with >= 100 citations published between 1998-2003
main_paper_with_citation = 'main_paper_with_citation'
main_paper_with_reference = 'main_paper_with_reference'
main_paper_with_abstract = 'main_paper_with_abstract'
other_paper_with_abstract = 'other_paper_with_abstract'