from ingestion import Ingestor

ingestor = Ingestor()

while True:
    try:
        ingestor.get_tag_data_json(tag_file='tags.txt')
    except Exception as e:
        print(f"ERROR: Ingestor-- {e.__str__()}")
