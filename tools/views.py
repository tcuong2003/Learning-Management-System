# views.py
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .forms import ExamGenerationForm
from tools.library.utils import generator, excel_to_json
import pandas as pd
from io import BytesIO
import zipfile
import json  # Import the json module

def generate_exams_view(request):
    if request.method == 'POST':
        form = ExamGenerationForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            number_of_exams = form.cleaned_data['number_of_exams']

            # Generate exams
            generated_files = []
            number_of_questions = {}
            
            # Read the Excel file to determine the number of questions per sheet
            excel_data = pd.ExcelFile(excel_file)
            sheet_names = excel_data.sheet_names
            
            for name in sheet_names:
                number_of_questions[name] = 20  # Adjust as needed

            for count in range(number_of_exams):
                output_file, df_combined = generator(excel_file, number_of_questions)
                json_output = excel_to_json(df_combined)

                generated_files.append((output_file, json_output, df_combined, f"Generated exam number {count + 1}:"))

            # Create ZIP file
            mem_zip = BytesIO()
            with zipfile.ZipFile(mem_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
                for id, (output_file, json_output, df_combined, message) in enumerate(generated_files):
                    zf.writestr(f'exam_{id + 1}.xlsx', output_file.getvalue())
                    zf.writestr(f'exam_{id + 1}.json', json_output)
            
            mem_zip.seek(0)

            response = HttpResponse(mem_zip, content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="exams.zip"'
            return response

    else:
        form = ExamGenerationForm()

    return render(request, 'generate_exams.html', {'form': form})

# extract to json
def excel_to_json(df):
    # Convert DataFrame to JSON
    return df.to_json(orient='records', lines=True)

def convert_exams_view(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            excel_data = pd.ExcelFile(excel_file)
            sheet_names = excel_data.sheet_names
            
            mem_zip = BytesIO()
            with zipfile.ZipFile(mem_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
                for name in sheet_names:
                    df = pd.read_excel(excel_file, sheet_name=name)
                    json_output = excel_to_json(df)
                    
                    # Add JSON file to ZIP
                    zf.writestr(f'{name}.json', json_output)
            
            mem_zip.seek(0)
            
            response = HttpResponse(mem_zip, content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="jsonfiles.zip"'
            return response
    else:
        form = ExcelUploadForm()

    return render(request, 'convert_exams.html', {'form': form})
