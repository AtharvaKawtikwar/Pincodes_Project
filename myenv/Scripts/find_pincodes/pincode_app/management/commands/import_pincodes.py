import pandas as pd
from django.core.management.base import BaseCommand
from pincode_app.models import Pincode

class Command(BaseCommand):
    help = 'Import pincodes from an Excel/CSV file'

    def handle(self, *args, **kwargs):
        # Replace with the path to your CSV or Excel file
        file_path = r"C:\Users\Atharva Kawtikwar\Downloads\pincode_dataset.csv"
        data = pd.read_csv(file_path)  # If you have an Excel file, use pd.read_excel()
        data.columns = data.columns.str.strip()  # Strip whitespace from column names

        print(data.columns)  # Print the DataFrame columns for debugging

        # Iterate over the rows and save them to the database
        for index, row in data.iterrows():
            try:
                # Use the correct column names for latitude and longitude
                longitude = row['Long'] if pd.notna(row['Long']) else None
                latitude = row['Lat'] if pd.notna(row['Lat']) else None

                # Use the correct column name for the pincode
                if pd.notna(row['Pin code']) and (longitude is not None or latitude is not None):
                    pincode, created = Pincode.objects.get_or_create(
                        pincode=row['Pin code'],
                        defaults={
                            'longitude': longitude,
                            'latitude': latitude,
                        }
                    )
                    if created:
                        self.stdout.write(f"Imported pincode: {pincode.pincode}")
                    else:
                        self.stdout.write(f"Pincode already exists: {pincode.pincode}")
                else:
                    self.stdout.write(f"Skipping row {index + 1} due to missing pincode or coordinates.")
            except Exception as e:
                self.stdout.write(f"Error importing pincode {row['Pin code']}: {e}")

        self.stdout.write("Import complete!")
