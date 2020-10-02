import xlrd

def Mohlenpris(filename):
    book = xlrd.open_workbook("mohlenpris-100.xlsx")
    sheet = book.sheet_by_index(0)

    # Seperate by solution type
    google_data = []
    NN_data = []
    greedy_data = []
    HC_data = []
    MK_data = []
    for row in range(1, 511):
        if "Google" in sheet.cell(row, 4):
            google_data.append(sheet.row(row))
        if "neighbor" in sheet.cell(row, 4):
            NN_data.append(sheet.row(row))
        elif "Greedy Clustering" in sheet.cell(row, 4):
            greedy_data.append(sheet.row(row))
        elif "MAHC" in sheet.cell(row, 4):
            HC_data.append(sheet.row(row))
        elif "MKMC" in sheet.cell(row, 4):
            MK_data.append(sheet.row(row))


    google_5 = google_data[0::3]
    google_10 = google_data[1::3]
    google_20 = google_data[2::3]

    NN_5 = NN_data[0::3]
    NN_10 = NN_data[1::3]
    NN_20 = NN_data[2::3]

    GC_5 = greedy_data[0::3]
    GC_10 = greedy_data[1::3]
    GC_20 = greedy_data[2::3]

    D_HC_5 = HC_data[0::3]


