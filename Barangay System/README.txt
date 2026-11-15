BARANGAY DOCUMENT REQUEST SYSTEM - PYTHON CLIENT (Flask)
Residents log in, view records, and manage their own document requests.

SETUP (PyCharm)
1. Open this folder as a PyCharm project and create a virtual environment.
2. Install:   pip install -r requirements.txt
3. Open db_config.py and set your MySQL password. The database name is db_barangay_system.
4. Run main.py.  Open  http://localhost:5050/

LOG-IN
Only accounts that have a ResidentID can sign in here. Create one in the ASP.NET site:
User > Add New User, with Status = Active and ResidentID = an existing resident's ID.
(Passwords are compared as plain text, as in class.)

PAGES (requirement 2.b)
 Record Viewing (Read-All and Read-One only)
   /read_all_doctype    /read_one_doctype/<id>     tbldocumenttype
   /read_all_resident   /read_one_resident/<id>    tblresident (own household only)
   /read_all_payment    /read_one_payment/<id>     tblpayment (own payments only)
 Transaction Management (Create, Read-All, Read-One, Update, Delete)
   /read_all_request  /create_request_view  /read_one_request/<id>
   /update_request_view/<id>  /delete_request_view/<id>        tblrequest

RULES
 - Every query uses the logged-in resident's ResidentID, so nobody can see another resident's data.
 - A request can be edited or cancelled only while its status is Pending.
 - A request that already has a Paid payment cannot be cancelled.
 - New requests get an ID like REQ-001, Status = Pending, and the current date and time.

POSTMAN (JSON API for tblrequest)
 1. POST  http://localhost:5050/log_in_user   body: x-www-form-urlencoded  Username, Password
    (Postman keeps the session cookie for the next calls.)
 2. GET     /api/requests            read all
    GET     /api/requests/REQ-001    read one
    POST    /api/requests            body (raw JSON): {"DocTypeID":"DOC-001","Purpose":"Employment","Remarks":""}
    PUT     /api/requests/REQ-001    body (raw JSON): {"DocTypeID":"DOC-001","Purpose":"Scholarship","Remarks":""}
    DELETE  /api/requests/REQ-001
