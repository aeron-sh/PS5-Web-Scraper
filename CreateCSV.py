import csv


def create_csv():
    file = open("tracker.csv", "w")
    writer = csv.writer(file)

    header = ["Time", "GameStop - DISC", "GameStop DIGI", "Amazon - DISC",
              "Amazon - DIGI", "Sony - DISC", "Sony - DIGI", "Canada Computers"]
    writer.writerow(header)
    file.close()


def write_from_data():
    file = open("data.txt", "r")
    data = file.readlines()
    file.close()

    lst_of_sites = []
    for line in data:
        temp = line[0:-1]
        temp_lst = temp.split("', '")
        lst_of_sites.append(temp_lst)

    new_input = [lst_of_sites[0][2], lst_of_sites[0][1], lst_of_sites[1][1],
                 lst_of_sites[2][1], lst_of_sites[3][1], lst_of_sites[4][1],
                 lst_of_sites[5][1], lst_of_sites[6][1]]

    f = open("tracker.csv", "a")
    writer = csv.writer(f)
    writer.writerow(new_input)
    f.close()
