# 🔍 XSEARCH v2.0
### Admin Panel Finder by @zaax | EXEL Framework

Tools pencari panel admin login otomatis dengan validasi real-time. No fake results, hanya panel yang valid yang ditampilkan.

---



## ✨ Fitur

| Fitur | Detail |
|-------|--------|
| **Real Validation** | Scoring system cek title, form, keywords, status code |
| **Multi-threaded** | Default 50 thread, bisa diatur |
| **User-Agent Rotation** | Anti-deteksi WAF |
| **Smart Filtering** | Filter out 404 pages & false positives |
| **Auto Save** | Hasil otomatis disimpan ke file |
| **CMS Detection** | WordPress, Joomla, Drupal, Magento, Laravel, Django, dll |
| **Color Output** | Terminal berwarna, mudah dibaca |
| **Progress Tracking** | Real-time progress counter |

---

## 🚀 Instalasi

```bash
# Clone/download file
git clone https://github.com/yourname/xsearch.git
cd xsearch

# Install dependencies
pip install -r requirements.txt


---

| Flag            | Description             | Default        |
| --------------- | ----------------------- | -------------- |
| `-u, --url`     | Target URL (wajib)      | -              |
| `-t, --threads` | Jumlah thread           | 50             |
| `--timeout`     | Timeout request (detik) | 8              |
| `-o, --output`  | File output             | auto-generated |
| `-v, --verbose` | Tampilkan semua request | False          |

