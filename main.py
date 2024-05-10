import streamlit as st
import openai
import gspread
from oauth2client.service_account import ServiceAccountCredentials

openai.api_key = 'YOUR_OPENAI_API_KEY'
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('YOUR_GOOGLE_SHEETS_CREDS.json', scope) 
gc = gspread.authorize(credentials)
sheet_name = 'YOUR_SHEET_NAME'
worksheet_name = 'Sheet1'
sh = gc.open(sheet_name)
worksheet = sh.worksheet(worksheet_name)

def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        temperature=0.7,
        n=1
    )
    return response.choices[0].text.strip()

def main():
    st.title("ChatGPT Response Generator")
    statements = worksheet.col_values(1)[1:]  
    responses = []
    for statement in statements:
        response = generate_response(statement)
        responses.append(response)
    worksheet.update('B2:B' + str(len(responses) + 1), [[response] for response in responses])

    st.write("Responses generated and updated in Google Sheets!")

if __name__ == "__main__":
    main()
