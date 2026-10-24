# Hospital Management System

A command-line app for keeping track of hospital patients, written in Python with a MySQL database behind it.

I built the first version as my Class 12 computer science project. It worked, but it was a bit of a mess: the database password was sitting in the code, one wrong keystroke crashed the whole thing, and you could "discharge" a patient before they were admitted. I came back to it as a first-year B.Tech student and cleaned it up properly, so this repo is the grown-up version.

## What it does

- **Add** a patient (with validation on every field)
- **View** everyone in a neat table
- **Search** by patient ID or by part of a name
- **Update** any single field of a record
- **Delete** a record, with a confirmation step

Things I made sure it handles: duplicate patient IDs, bad dates, discharge dates before admission dates, empty input, letters typed where numbers belong, and patients who haven't been discharged yet.

## Getting started

You need Python 3.9+ and a running MySQL server.

```bash
git clone https://github.com/<your-username>/hospital-management-system.git
cd hospital-management-system
pip install -r requirements.txt
```

Tell the app how to reach your database using environment variables (never hard-code your password):

```bash
# Linux / macOS
export DB_PASSWORD="your_mysql_password"

# Windows (PowerShell)
$env:DB_PASSWORD = "your_mysql_password"
```

Optional: `DB_HOST` (default `localhost`), `DB_USER` (default `root`), `DB_NAME` (default `hospital`). See `.env.example`.

Then run it:

```bash
python hospital.py
```

The database and table are created automatically on first run. If you'd rather set them up by hand, `schema.sql` has the same structure.

## What a patient record holds

| Field | Notes |
|---|---|
| Patient ID | Unique whole number |
| Name, diagnosis, doctor, department | Text, length-checked |
| Age | 0 to 130 |
| Contact number | 10 to 15 digits |
| Admission date | `YYYY-MM-DD` |
| Discharge date | Optional until the patient leaves |
| Fees | Stored as `DECIMAL`, not float, so money stays exact |
| Payment status | Paid / Pending / Partial |

## What changed from the Class 12 version

- Password moved out of the code into environment variables
- Fees use `DECIMAL(10,2)` instead of `FLOAT`
- Discharge date can be empty for current patients
- All input is validated and re-asked instead of crashing
- One field definition drives both "add" and "update", so no copy-pasted blocks
- Parameterised queries everywhere; the only dynamic column name comes from a fixed whitelist
- Added delete and name search, removed the pointless "continue? (y/n)" after every action

## Ideas for later

- Reports (outstanding dues, patients per department)
- A simple web front end with Flask
- Unit tests for the input parsers

## License

MIT. Do what you like with it.
