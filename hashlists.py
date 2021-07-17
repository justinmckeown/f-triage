import csv

class Hashlists:
    def __init__(self, name, hashes, report) -> None:
        self.name = name
        self.hashes = hashes
        self.report = report
        self.log = []
    
    def write_report(self, write_path):
        with open(write_path, 'a', newline='') as csvf:
            reportwriter = csv.writer(csvf)
            print(f'Write report called. Report has {len(self.report)} entries')
            if len(self.report):
                reportwriter.writerow(['ENTRY NUMBER', 'NYP HASH LIST NAME', 'MATCHED HASH' ,'MATCHED TO FILE', 'DETECTION DATE-TIME'])
                for i, row in enumerate(self.report):
                    reportwriter.writerow([i, row[0], row[1], row[2], row[3]])
            else:
                reportwriter.writerow([0,f'{len(self.hashes)} hashes from the {self.name} hash list were compared to hashes of files on the target machine. No matches were found'])

    
    def write_error_logs(self, write_path):
        with open(write_path, 'a', newline='') as csvf:
            reportwriter = csv.writer(csvf)
            if len(self.log):
                for i, row in enumerate(self.log):
                    reportwriter.writerow([i, row])


    