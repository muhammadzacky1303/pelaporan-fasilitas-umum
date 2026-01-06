import requests

SUPABASE_URL = "https://nphemegpwmwkoswftyet.supabase.co"
SUPABASE_KEY = "sb_publishable_5qbPXobQ9r-L-nZRoBlg8Q_Pae6M1xx"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# =========================
# INSERT DATA
# =========================
def insert_laporan(data):
    url = f"{SUPABASE_URL}/rest/v1/laporan"
    response = requests.post(url, headers=HEADERS, json=data)
    return response.status_code, response.text


# =========================
# GET DATA
# =========================
def get_laporan():
    url = f"{SUPABASE_URL}/rest/v1/laporan?select=*"
    response = requests.get(url, headers=HEADERS)
    return response.json()


# =========================
# UPDATE STATUS LAPORAN
# =========================
def update_status_laporan(id_laporan, status_baru):
    url = f"{SUPABASE_URL}/rest/v1/laporan?id=eq.{id_laporan}"
    data = {
        "status": status_baru
    }
    response = requests.patch(url, headers=HEADERS, json=data)
    return response.status_code


# =========================
# DELETE LAPORAN
# =========================
def delete_laporan(id_laporan):
    url = f"{SUPABASE_URL}/rest/v1/laporan?id=eq.{id_laporan}"
    response = requests.delete(url, headers=HEADERS)
    return response.status_code
