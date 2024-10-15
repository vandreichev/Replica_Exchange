import os
import glob

def format_with_sign(value):
    value_float = float(value)
    if value_float >= 0:
        return f"+{value_float}"
    return str(value_float)

def split_files():
    input_files = glob.glob('dat/*.dat')
    for input_file in input_files:
        base_name = os.path.splitext(input_file)[0]
        phi_file = base_name + '.phi'
        psi_file = base_name + '.psi'

        with open(input_file, 'r') as file:
            phi_lines = []
            psi_lines = []

            for line in file:
                phi_value, psi_value = line.strip().split()

                formatted_phi = format_with_sign(phi_value)
                formatted_psi = format_with_sign(psi_value)
                phi_lines.append(formatted_phi)
                psi_lines.append(formatted_psi)

        with open(phi_file, 'w') as file:
            file.write('\n'.join(phi_lines) + '\n')

        with open(psi_file, 'w') as file:
            file.write('\n'.join(psi_lines) + '\n')

        print(f"Created {phi_file} and {psi_file} from {input_file}")

split_files()
