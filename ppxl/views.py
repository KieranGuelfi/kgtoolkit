from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from io import BytesIO

from .forms import UploadReportForm

# Create your views here.


def upload_file(request):
    if request.method == 'POST':

        form = UploadReportForm(request.POST, request.FILES)

        # Return the report as a file object
        report = request.FILES['report']

        # Definition of mptpdict, which is a dictionary of the MPTP for each pharmaprogram item
        mptpdict = {
            "BRINTELLIX TAB 5MG BLST 28": 64.98,
            "BRINTELLIX TAB 10MG BLST 28": 64.98,
            "BRINTELLIX TAB 15MG BLST 28": 74.98,
            "BRINTELLIX TAB 20MG BLST 28": 84.98,
            "LOCERYL NLACQ KIT 5ML": 64.95,
            "NUROFEN C&F TAB 24": 22.98,
            "NUROFEN PLUS TAB 30 (S4)": 19.98
        }

        # Convert the file object to a Pandas dataframe
        ppsales = pd.read_excel(report)

        # Convert row 6 to headers, removing the header from the ID column
        ppsales.columns = ppsales.iloc[5]
        ppsales = ppsales.rename_axis(None, axis="columns")

        # Create string for naming the final exported file
        # Split the cell of the input file containing date information and retains only the 'Mon' and 'YY' elements in a list
        daterangelist = ppsales.iloc[3, 0].split()[4:6]
        # Add '777 PharmaProgram Sales' element to the start of the list
        daterangelist.insert(0, '777 PharmaProgram Sales')
        # Join all list elements together by a space
        daterange = ' '.join(daterangelist)
        # Store final string in filename variable with .xlsx at the end
        filename = daterange + '.xlsx'

        # Drop empty rows from start of dataframe
        ppsales = ppsales.drop([0, 1, 2, 3, 4, 5])

        # Drop rows containing Lagevrio
        ppsales = ppsales[ppsales["Description"].str.contains(
            "LAGEVRIO 200MG 40 CAPS") == False]

        # Drop final row that contains summary information
        ppsales.drop(ppsales.tail(1).index, inplace=True)

        # Drop irrelevant columns from dataframe and rename sales column
        ppsales = ppsales.drop(
            columns=['Category', 'Item\nID', 'Cost Ex', 'Sales Ex', 'HIC', 'GP $', 'GP %'])
        ppsales.rename(
            columns={'Total\nSales Ex': 'Total Sales Ex'}, inplace=True)

        # Change datatypes of columns
        ppsales[['Qty', 'Total Sales Ex']] = ppsales[[
            'Qty', 'Total Sales Ex']].apply(pd.to_numeric)

        # Create new column indicating item cost
        ppsales['Price'] = ppsales['Total Sales Ex']/ppsales['Qty']

        # Create column called MPTPDiff that calculates the difference between Maximum Price To Patient(MPTP) and actual price
        ppsales['MPTPDiff'] = ppsales['Price'] - \
            ppsales['Description'].map(mptpdict)

        # Replace all instances of an MPTPDiff between 0 and 5 with the exact MPTP
        # In other words, for close differences under $5, we adjust to the actual MPTP
        ppsales.loc[ppsales['MPTPDiff'].between(
            0, 5), 'Price'] = ppsales['Description'].map(mptpdict)

        # Recalculate MPTPDiff to account for new Price
        ppsales['MPTPDiff'] = ppsales['Price'] - \
            ppsales['Description'].map(mptpdict)

        # Recalculate Total Sales Ex to correctly reflect new Price
        ppsales['Total Sales Ex'] = ppsales['Qty']*ppsales['Price']

        # Drop all rows that 'take the piss', which have an MPTPDiff > $5
        ppsales = ppsales.drop(ppsales[ppsales['MPTPDiff'] > 0].index)

        # Drop all rows that have a Total Sales Ex of 0 for some reason
        ppsales = ppsales.drop(ppsales[ppsales['Total Sales Ex'] == 0].index)

        # Reset index column to adjust for deleted rows
        # (this just cleans up the dataframe view and doesn't affect the final export)
        ppsales = ppsales.reset_index(drop=True)

        # Drop MPTPDiff column
        ppsales = ppsales.drop(columns=['MPTPDiff'])

        # Export to .xlsx

        with BytesIO() as b:
            writer = pd.ExcelWriter(b, engine='xlsxwriter')
            ppsales.to_excel(writer, sheet_name='SalesByItem',
                             float_format="%.2f", index=False)
            for column in ppsales:
                column_length = max(ppsales[column].astype(
                    str).map(len).max(), len(column))
                col_idx = ppsales.columns.get_loc(column)
                writer.sheets['SalesByItem'].set_column(
                    col_idx, col_idx, column_length)
            writer.save()
            response = HttpResponse(b.getvalue(
            ), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=%s' % filename
            return response
    else:
        form = UploadReportForm
        # This makes the Upload button appear
        show_link = True
    return render(request, 'ppxl.html', {'form': form})


def mptpedit(request):
    return render(request, 'mptp.html', {})
