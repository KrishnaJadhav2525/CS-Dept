# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-02-04
**Fully fixed, improved, and connected to MongoDB Atlas.**

### Fixed
- **Database Connection**: Resolved `SSL handshake failed` errors on Windows by upgrading environment to Python 3.14 (OpenSSL 3.0+).
- **Configuration**: Fixed `pymongo.errors.ConfigurationError` by correctly specifying the default database name (`csdept`) in `MONGO_URI`.
- **Dependencies**: Added `certifi` package to handle SSL certificate verification in the new environment.
- **Git Ignore**: Added `.gitignore` to exclude temporary files and cache.

### Changed
- **Code Quality**: Refactored imports in `app.py` to follow PEP 8 standards.
- **Documentation**: Added docstrings to `Database` class in `db.py` for better clarity.
- **Frontend**: Fixed CSS linter errors and improved semantic HTML in `about.html`.
