import re
import glob

def extract_data():

    log_files = sorted(glob.glob('logs/*.log'), key=lambda x: int(x.split('/')[-1].split('.')[0]))


    new_tag_lines = []
    epot_lines = []


    for file_idx, log_file in enumerate(log_files):
        with open(log_file, 'r') as file:
            new_tag_values = []
            epot_values = []


            for line in file:

                new_tag_match = re.search(r'REX>ORIGINAL TAG\s+\d+\s+NEW TAG\s+(\d+)', line)
                if new_tag_match:
                    new_tag_values.append(int(new_tag_match.group(1)))


                epot_match = re.search(r'REX>REPL\s+=\s+\d+\s+Temp\s+=\s+\d+\.\d+\s+Epot\s+=\s+([-\d\.]+)', line)
                if epot_match:
                    epot_values.append(float(epot_match.group(1)))


            if file_idx == 0:
                new_tag_lines = [[value] for value in new_tag_values]
                epot_lines = [[value] for value in epot_values]
            else:

                for i, value in enumerate(new_tag_values):
                    new_tag_lines[i].append(value)
                for i, value in enumerate(epot_values):
                    epot_lines[i].append(value)

    with open('replica-indices', 'w') as new_tag_file:
        for line in new_tag_lines:
            new_tag_file.write(' '.join(map(str, line)) + '\n')

    with open('energies/potential-energies', 'w') as epot_file:
        for line in epot_lines:
            epot_file.write(' '.join(map(str, line)) + '\n')

    print("Extraction complete! The data has been saved to replica-indices and energies/potential-energies")

extract_data()
