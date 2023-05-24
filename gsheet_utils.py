import gspread
import pandas as pd
import gspread_dataframe as gd
import os


def export_to_sheets(ws,df=None,mode='r'):
    if mode == 'w':
        ws.clear()
        gd.set_with_dataframe(worksheet=ws,dataframe=df,include_index=False,include_column_header=True,resize=True)
        return True
    elif mode == 'a':
        ws.add_rows(df.shape[0])
        gd.set_with_dataframe(worksheet=ws,dataframe=df,include_index=False,include_column_header=False,row=ws.row_count+1,resize=False)
        return True
    else:
        return gd.get_as_dataframe(worksheet=ws)

def clear_sheet(ws, keep_headers):
    if keep_headers:
        # Get the number of rows in the worksheet
        num_rows = ws.row_count

        # Delete all rows except for the first one (header row)
        if num_rows > 1: 
            ws.delete_rows(2, num_rows)
    else:
        ws.clear()

def access_gsheet(auth_json='anki-359920-d78c1a86928f.json', file_name='Async Translate',
                  sheet_name='Translations'):
    sa = gspread.service_account(auth_json)
    sh = sa.open(file_name)
    wks = sh.worksheet(sheet_name)
    return pd.DataFrame(wks.get_all_records()), wks


def access_gsheet_by_url(auth_json='anki-359920-d78c1a86928f.json', url='Async Translate',
                  sheet_name='Translations'):
    sa = gspread.service_account(auth_json)
    sh = sa.open_by_url(url)
    wks = sh.worksheet(sheet_name)
    return pd.DataFrame(wks.get_all_records()), wks

def return_unprocessed_data_to_gsheet(unprocessed_df, wks):
    export_to_sheets(wks, unprocessed_df, mode='w')


def remove_rows_with_empty(df):
    # this is actually very specific to this program, but gsheet_utils seems like most reasonable place to put it
    if df.empty:
        return
    unprocessed_df = df.copy(deep=True)  # the df that'll be put back into the spreadsheet since its rows aren't yet filled out
    invalid_row_0_mask = df['English'] == ''
    invalid_row_1_mask = df['Simplified'] == ''
    df.drop(df[invalid_row_0_mask].index, inplace=True)
    #df.reset_index(inplace=True, drop=True)
    df.drop(df[invalid_row_1_mask].index, inplace=True)
    df.reset_index(inplace=True, drop=True)
    unprocessed_df.drop(unprocessed_df[~invalid_row_0_mask & ~invalid_row_1_mask].index, inplace=True)
    return unprocessed_df, df


def log_df(processed_df, csv_filename):
    # always keep track of a file containing a df with all the gsheet data
    if not os.path.exists(csv_filename):
        processed_df.to_csv(csv_filename, sep='\t')
    else:
        processed_df.to_csv(csv_filename, mode='a', index=False, header=False, sep='\t')