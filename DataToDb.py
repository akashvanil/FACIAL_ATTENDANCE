import firebase_admin
from firebase_admin import credentials, db

# Provide the correct path to your service account key JSON file
cred = credentials.Certificate("serviceAccountKey.json")

# Replace with your actual database URL from Firebase
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://rtu-attendance-31d29-default-rtdb.firebaseio.com/'
})

ref = db.reference('students')  # This should now work


data = {
    "34011":{
        "name":"Ashwin Sunil",
        "Group":"Computer science",
        "level":"bachelor",
        "study cycle":" 3rd ",
        "total attendance":"5",
        "recent_attendance_time":"2025-03-01 00:54:34"


    },
    "34021":{
        "name":"Souvik Adhikary",
        "Group":"IT",
        "level":"master",
        "study cycle":" 1st ",
        "total attendance":"1",
        "recent_attendance_time":"2025-03-01 00:54:34"


    },
    "34031":
        {
        "name":"Meenakshi Gireesh",
        "Group":"IT",
        "level":"bachelor",
        "study cycle":" 4th ",
        "total attendance":"8",
        "recent_attendance_time":"2025-03-01 00:54:34"


    },
    "34041":{
        "name":"Akash V Anil",
        "Group":"Computer Science",
        "level":"bachelor",
        "study cycle":" 3rd ",
        "total attendance":"7",
        "recent_attendance_time":"2025-03-01 00:54:34"


    },
    "34051":{
        "name":"Gleniya Paul",
        "Group":"IT",
        "level":"master",
        "study cycle":" 1st ",
        "total attendance":"8",
        "recent_attendance_time":"2025-03-01 00:54:34"


    }

}
for key, value in data.items():
    ref.child(key).set(value)