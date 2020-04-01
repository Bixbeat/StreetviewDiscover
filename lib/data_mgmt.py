import csv

def export_to_csv(out_filepath, record_list):
    """Simple utility to export SQLite records to a CSV
    
    Arguments:
        out_filepath {str} -- Filepath+name of output file
        record_list {list} -- List of lists containing SQLite database records
    """    
    with open("out_filepath", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(record_list)    