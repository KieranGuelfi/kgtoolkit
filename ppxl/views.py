from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
import pandas as pd
from io import BytesIO

from .forms import UploadReportForm

from .models import MPTP


# Create your views here.

class MPTPList(ListView):
    model = MPTP


def upload_file(request):
    if request.method == 'POST':

        form = UploadReportForm(request.POST, request.FILES)

        # Return the report as a file object
        report = request.FILES['report']

        # Creates itemlist, which is simply a list of all PharmaProgram items regardless of a MPTP
        # Also creates mptpdict, which is a dictionary of all PharmaProgram items currently in the database that have an MPTP condition
        itemlist = []
        mptpdict = {}
        for item in MPTP.objects.all():
            itemlist.append(item.itemdesc)
            if item.mptp_applies is True:
                mptpdict[item.itemdesc] = item.mptp

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

        # Create an empty 'droplist' variable which will contain information of all dropped rows
        droplist = []

        # Drop empty rows from start of dataframe. Add dropped rows to droplist
        droplist.append(["Irrelevant starting rows dropped:"])
        droplist.append(ppsales.iloc[[0, 1, 2, 3, 4, 5]].values.tolist())
        ppsales = ppsales.drop([0, 1, 2, 3, 4, 5])

        # Drop any rows for items not currently in the mptp dictionary (e.g., Lagevrio)
        # This will help future proof to save needing to make sure that the initial report contains only current PharmaProgram items
        ppsales = ppsales[ppsales['Description'].isin(itemlist)]

        # Drop final row that contains summary information. Add dropped row to droplist
        droplist.append(["Final row dropped:"])
        droplist.append(ppsales.tail(1).values.tolist())
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
        # Save rows as pisstakes for later auditing
        droplist.append(
            ["Removed for having too high a difference from MPTP:"])
        droplist.append(ppsales[ppsales['MPTPDiff'] > 0].values.tolist())
        ppsales = ppsales.drop(ppsales[ppsales['MPTPDiff'] > 0].index)

        # Drop all rows that have a Total Sales Ex of 0 for some reason, if there are any
        # Add row(s) if any to droplist
        if ppsales[ppsales['Total Sales Ex'] == 0].size > 0:
            droplist.append(["Removed for having Total Sales Ex = 0"])
            droplist.append(
                ppsales[ppsales['Total Sales Ex'] == 0].values.tolist())
            ppsales = ppsales.drop(
                ppsales[ppsales['Total Sales Ex'] == 0].index)
        else:
            pass

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
            for sublist in droplist:
                for subsublist in sublist:
                    if len(sublist) > 1:
                        messages.error(request, subsublist)
                    else:
                        messages.error(request, sublist)
            return response
    else:
        form = UploadReportForm
        # This makes the Upload button appear
        show_link = True
    return render(request, 'ppxl/ppxl.html', {'form': form})
