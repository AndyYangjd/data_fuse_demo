import xlrd3


def getData(file_pth=None):
    if file_pth is not None:
        xf = xlrd3.open_workbook(file_pth)

        return_data = []
        for id_sh in range(xf.nsheets):
            sh = xf.sheet_by_index(id_sh)

            x = sh.col_values(0)[1:]
            y = sh.col_values(1)[1:]
            vx_comp = sh.col_values(8)[1:]
            vy_comp = sh.col_values(9)[1:]

            current_data = {
                "x": x,
                "y": y,
                "vx_compy": vx_comp,
                "vy_compy": vy_comp
            }
            return_data.append(current_data)

        return return_data
    else:
        print("Plse input the xls-path")