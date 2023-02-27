import xlsxwriter

'''
This function writes the desired and simulated cashflows to an excel file with a chosen name
The first sheet of this files contains the desired cashflows
The second sheet contains the simulated cashflows

Input:  name_file -> name of the output file
        desired -> 1D-array with the desired cashflows
        simulated -> XD-array with X simulated cashflow runs
'''


def writeCashflows(name_file, desired, simulated, interest_rates):
    wb = xlsxwriter.Workbook(name_file + '.xlsx')
    # First write the desired cashflows
    ws = wb.add_worksheet('Desired CF')
    months = [i + 1 for i in range(len(desired))]
    ws.write('A1', 'Months')
    ws.write('B1', 'Desired CF')
    ws.write_column('A2', months)
    ws.write_column('B2', desired)

    # Now, write the simulated cashflows to a seperate sheet
    ws = wb.add_worksheet('Simulated CF')
    runs = [i + 1 for i in range(len(simulated))]
    ws.write('A1', 'Months/Runs')
    ws.write_row('B1', runs)
    ws.write_column('A2', months)
    count_col = 1
    for sim in simulated:
        ws.write_column(1, count_col, sim)
        count_col += 1

    ws = wb.add_worksheet('Simulated Interest Rates')
    runs = [i + 1 for i in range(len(interest_rates))]
    ws.write('A1', 'Months/Runs')
    ws.write_row('B1', runs)
    ws.write_column('A2', months)
    count_col = 1
    for rate in interest_rates:
        ws.write_column(1, count_col, rate)
        count_col += 1
    wb.close()


'''
This function writes the hedge of certain instrument(s) to an excel file

input:  file_name -> name of the output file
        hedge -> array containing number of required elements per instrument for the hedge
        maturities -> array containing maturities of the different types of instruments
        type_instr -> type of instrument(s) used in the hedge, must contain string elements
'''
def writeHedge(file_name, hedge, maturities, type_instr):
    wb = xlsxwriter.Workbook(file_name + '.xlsx')
    ws = wb.add_worksheet('Hedge with' + ' '.join(type_instr))
    col_count = 0
    for i in range(len(type_instr)):
        ws.write(0, col_count, type_instr[i])
        ws.write_column(1, col_count, maturities[i])
        ws.write_column(1, col_count+1, hedge[i])
        col_count += 2
    wb.close()
