import os, json
from datetime import datetime
try:
    from pymongo import MongoClient
    import certifi
    import gridfs
except Exception:
    MongoClient = None
    certifi = None


class Database:
    """
    Handles database interactions, supporting both MongoDB (remote) 
    and proper local JSON file storage as a fallback.
    """
    def __init__(self, use_mongo=False, mongo_uri=''):
        self.use_mongo = use_mongo and MongoClient is not None
        self.mongo_uri = mongo_uri
        self.file = os.path.join(os.getcwd(), 'database.json')

        if not self.use_mongo:
            # JSON file mode
            if not os.path.exists(self.file):
                initial = {
                    'students': [],
                    'blogs': [],
                    'contacts': [],
                    'faculty': [],
                    'events': [],
                    'notifications': [],
                    'gallery': [],
                    'research': [],
                    'csa_members': [],
                    'past_csa': [],
                    'curriculum':[],
                    'alumni':[]
                }
                with open(self.file, 'w') as f:
                    json.dump(initial, f, indent=2)
        else:
            # MongoDB mode - disable SSL verification for Windows compatibility
            # (Python 3.10 on Windows has an old OpenSSL that fails TLS handshake with Atlas)
            self.client = MongoClient(self.mongo_uri, tlsAllowInvalidCertificates=True)
            self.db = self.client.get_default_database()
            self.fs = gridfs.GridFS(self.db)

    # ---------- JSON helpers ----------
    def _read(self):
        with open(self.file, 'r') as f:
            return json.load(f)

    def _write(self, data):
        with open(self.file, 'w') as f:
            json.dump(data, f, indent=2, default=str)

    # ---------- GRIDFS HELPERS ----------
    def save_file(self, filename, file_data, content_type=None):
        """
        Saves file data to GridFS and returns the file ID as a string.
        """
        if self.use_mongo:
            file_id = self.fs.put(file_data, filename=filename, content_type=content_type)
            return str(file_id)
        return None

    def get_file(self, file_id):
        """
        Retrieves file from GridFS. Returns (data_bytes, content_type, filename) or None.
        """
        if self.use_mongo:
            try:
                from bson.objectid import ObjectId
                f = self.fs.get(ObjectId(file_id))
                return f.read(), f.content_type, f.filename
            except Exception:
                return None
        return None

    # ---------- STUDENTS ----------
    def add_student(self, student):
        if self.use_mongo:
            return self.db.students.insert_one(student).inserted_id
        d = self._read()
        student.setdefault('is_active', True)
        d.setdefault('students', []).append(student)
        self._write(d)
        return student.get('id')

    def list_students(self):
        if self.use_mongo:
            students = list(self.db.students.find())
            for s in students:
                s.pop('_id', None)
            return students
        return self._read().get('students', [])

    def find_student_by_email(self, email):
        if self.use_mongo:
            return self.db.students.find_one({'email': email})
        d = self._read()
        for s in d.get('students', []):
            if s.get('email') == email:
                return s
        return None

    def find_student_by_student_id(self, student_id):
        if self.use_mongo:
            return self.db.students.find_one({'student_id': student_id})
        d = self._read()
        for s in d.get('students', []):
            if s.get('student_id') == student_id:
                return s
        return None

    def update_student(self, student_id, changes):
        if self.use_mongo:
            return self.db.students.update_one({'id': student_id}, {'$set': changes})
        d = self._read()
        for i, s in enumerate(d.get('students', [])):
            if s.get('id') == student_id:
                d['students'][i].update(changes)
                self._write(d)
                return True
        return False

    def delete_student(self, student_id):
        if self.use_mongo:
            return self.db.students.delete_one({'id': student_id})
        d = self._read()
        d['students'] = [s for s in d.get('students', []) if s.get('id') != student_id]
        self._write(d)
        return True

    # ---------- BLOGS ----------
    def add_blog(self, blog):
        if self.use_mongo:
            return self.db.blogs.insert_one(blog).inserted_id
        d = self._read()
        d.setdefault('blogs', []).append(blog)
        self._write(d)
        return blog.get('id')

    def list_blogs(self, approved_only=True, status=None):
        if self.use_mongo:
            q = {}
            if approved_only:
                q['status'] = 'approved'
            if status:
                q['status'] = status
            blogs = list(self.db.blogs.find(q))
            for b in blogs:
                b.pop('_id', None)
            return blogs
        d = self._read()
        blogs = d.get('blogs', [])
        if status:
            blogs = [b for b in blogs if b.get('status') == status]
        if approved_only and not status:
            blogs = [b for b in blogs if b.get('status') == 'approved' or b.get('approved')]
        return blogs

    def get_blog(self, blog_id):
        if self.use_mongo:
            blog = self.db.blogs.find_one({'id': blog_id})
            if blog:
                blog.pop('_id', None)
            return blog
        d = self._read()
        for b in d.get('blogs', []):
            if b.get('id') == blog_id:
                return b
        return None

    def update_blog(self, blog_id, changes):
        if self.use_mongo:
            return self.db.blogs.update_one({'id': blog_id}, {'$set': changes})
        d = self._read()
        for i, b in enumerate(d.get('blogs', [])):
            if b.get('id') == blog_id:
                d['blogs'][i].update(changes)
                self._write(d)
                return True
        return False

    def delete_blog(self, blog_id):
        if self.use_mongo:
            return self.db.blogs.delete_one({'id': blog_id})
        d = self._read()
        d['blogs'] = [b for b in d.get('blogs', []) if b.get('id') != blog_id]
        self._write(d)
        return True

    # ---------- CONTACTS ----------
    def add_contact(self, contact):
        if self.use_mongo:
            return self.db.contacts.insert_one(contact).inserted_id
        d = self._read()
        d.setdefault('contacts', []).append(contact)
        self._write(d)
        return contact.get('id')

    def list_contacts(self):
        if self.use_mongo:
            contacts = list(self.db.contacts.find())
            for c in contacts:
                c.pop('_id', None)
            return contacts
        return self._read().get('contacts', [])

    def update_contact(self, contact_id, changes):
        if self.use_mongo:
            return self.db.contacts.update_one({'id': contact_id}, {'$set': changes})
        d = self._read()
        for i, c in enumerate(d.get('contacts', [])):
            if c.get('id') == contact_id:
                d['contacts'][i].update(changes)
                self._write(d)
                return True
        return False

    def delete_contact(self, contact_id):
        if self.use_mongo:
            return self.db.contacts.delete_one({'id': contact_id})
        d = self._read()
        d['contacts'] = [c for c in d.get('contacts', []) if c.get('id') != contact_id]
        self._write(d)
        return True

    # ---------- NOTIFICATIONS ----------
    def add_notification(self, n):
        if self.use_mongo:
            return self.db.notifications.insert_one(n).inserted_id
        d = self._read()
        d.setdefault('notifications', []).append(n)
        self._write(d)
        return n.get('id')

    def list_notifications(self):
        if self.use_mongo:
            # Sort by _id descending (newest first)
            notes = list(self.db.notifications.find().sort('_id', -1))
            for n in notes:
                n.pop('_id', None)
            return notes
        # Reverse list so newest (appended last) come first
        return self._read().get('notifications', [])[::-1]

    def update_notification(self, nid, changes):
        if self.use_mongo:
            return self.db.notifications.update_one({'id': nid}, {'$set': changes})
        d = self._read()
        for i, n in enumerate(d.get('notifications', [])):
            if n.get('id') == nid:
                d['notifications'][i].update(changes)
                self._write(d)
                return True
        return False

    def delete_notification(self, nid):
        if self.use_mongo:
            return self.db.notifications.delete_one({'id': nid})
        d = self._read()
        d['notifications'] = [n for n in d.get('notifications', []) if n.get('id') != nid]
        self._write(d)
        return True

    # ---------- FACULTY ----------
    def add_faculty(self, f):
        if self.use_mongo:
            return self.db.faculty.insert_one(f).inserted_id
        d = self._read()
        d.setdefault('faculty', []).append(f)
        self._write(d)
        return f.get('id')

    def list_faculty(self):
        if self.use_mongo:
            faculty = list(self.db.faculty.find())
            for f in faculty:
                f.pop('_id', None)
            return faculty
        return self._read().get('faculty', [])

    def update_faculty(self, fid, changes):
        if self.use_mongo:
            return self.db.faculty.update_one({'id': fid}, {'$set': changes})
        d = self._read()
        for i, f in enumerate(d.get('faculty', [])):
            if f.get('id') == fid:
                d['faculty'][i].update(changes)
                self._write(d)
                return True
        return False

    def delete_faculty(self, fid):
        if self.use_mongo:
            return self.db.faculty.delete_one({'id': fid})
        d = self._read()
        d['faculty'] = [f for f in d.get('faculty', []) if f.get('id') != fid]
        self._write(d)
        return True

    # ---------- EVENTS ----------
    def add_event(self, e):
        if self.use_mongo:
            return self.db.events.insert_one(e).inserted_id
        d = self._read()
        d.setdefault('events', []).append(e)
        self._write(d)
        return e.get('id')

    def list_events(self):
        if self.use_mongo:
            events = list(self.db.events.find())
            for e in events:
                e.pop('_id', None)
            return events
        return self._read().get('events', [])

    def update_event(self, eid, changes):
        if self.use_mongo:
            return self.db.events.update_one({'id': eid}, {'$set': changes})
        d = self._read()
        for i, e in enumerate(d.get('events', [])):
            if e.get('id') == eid:
                d['events'][i].update(changes)
                self._write(d)
                return True
        return False

    def delete_event(self, eid):
        if self.use_mongo:
            return self.db.events.delete_one({'id': eid})
        d = self.__read()
        d['events'] = [e for e in d.get('events', []) if e.get('id') != eid]
        self._write(d)
        return True

    # ---------- GALLERY ----------
    def add_gallery(self, g):
        if not isinstance(g, dict):
            return
        if not g.get('title') and not g.get('image'):
            return
        if self.use_mongo:
            return self.db.gallery.insert_one(g).inserted_id
        d = self._read()
        d.setdefault('gallery', []).append(g)
        self._write(d)
        return g.get('id')

    def list_gallery(self):
        if self.use_mongo:
            # Sort by _id descending (newest first)
            gallery = list(self.db.gallery.find().sort('_id', -1))
            for g in gallery:
                g.pop('_id', None)
            return gallery
        # Reverse list so newest (appended last) come first
        return self._read().get('gallery', [])[::-1]

    def delete_gallery(self, gid):
        if self.use_mongo:
            return self.db.gallery.delete_one({'id': gid})
        d = self._read()
        d['gallery'] = [g for g in d.get('gallery', []) if g.get('id') != gid]
        self._write(d)
        return True

    # ---------- RESEARCH ----------
    def add_research(self, r):
        if self.use_mongo:
            return self.db.research.insert_one(r).inserted_id
        d = self._read()
        d.setdefault('research', []).append(r)
        self._write(d)
        return r.get('id')

    def list_research(self):
        if self.use_mongo:
            research = list(self.db.research.find())
            for r in research:
                r.pop('_id', None)
            return research
        return self._read().get('research', [])

    def delete_research(self, rid):
        if self.use_mongo:
            return self.db.research.delete_one({'id': rid})
        d = self._read()
        d['research'] = [r for r in d.get('research', []) if r.get('id') != rid]
        self._write(d)
        return True

    # ---------- CSA MEMBERS ----------
    def list_csa_members(self):
        if self.use_mongo:
            members = list(self.db.csa_members.find())
            for m in members:
                m.pop('_id', None)
            return members
        return self._read().get('csa_members', [])

    def add_csa_member(self, m):
        if self.use_mongo:
            return self.db.csa_members.insert_one(m).inserted_id
        d = self._read()
        d.setdefault('csa_members', []).append(m)
        self._write(d)
        return m.get('id')

    def update_csa_member(self, mid, changes):
        if self.use_mongo:
            return self.db.csa_members.update_one({'id': mid}, {'$set': changes})
        d = self._read()
        for i, m in enumerate(d.get('csa_members', [])):
            if m.get('id') == mid:
                d['csa_members'][i].update(changes)
                self._write(d)
                return True
        return False

    def delete_csa_member(self, mid):
        if self.use_mongo:
            return self.db.csa_members.delete_one({'id': mid})
        d = self._read()
        d['csa_members'] = [m for m in d.get('csa_members', []) if m.get('id') != mid]
        self._write(d)
        return True

    # ---------- PAST CSA (PDF per year) ----------
    def list_past_csa(self):
        if self.use_mongo:
            past_csa = list(self.db.past_csa.find())
            for p in past_csa:
                p.pop('_id', None)
            return past_csa
        data = self._read()
        return data.get('past_csa', [])

    def add_past_csa(self, entry):
        if self.use_mongo:
            return self.db.past_csa.insert_one(entry).inserted_id
        data = self._read()
        items = data.get('past_csa', [])
        items.append(entry)
        data['past_csa'] = items
        self._write(data)
        return entry.get('id')

    def delete_past_csa(self, entry_id):
        if self.use_mongo:
            return self.db.past_csa.delete_one({'id': entry_id})
        data = self._read()
        items = data.get('past_csa', [])
        items = [e for e in items if e.get('id') != entry_id]
        data['past_csa'] = items
        self._write(data)
        return True
    # ---------- CURRICULUM / SYLLABUS ----------
    def list_curriculum(self):
        if self.use_mongo:
            records = list(self.db.curriculum.find())
            for r in records:
                r.pop("_id", None)   # 🔥 REMOVE ObjectId
            return records

        data = self._read()
        return data.get('curriculum', [])


    def add_or_update_curriculum(self, entry):
        """
        entry = {
          'degree': 'B.Sc. F.Y.',
          'year': '2024-25',
          'pdf_url': '/static/uploads/syllabus/xyz.pdf',
          'uploaded_at': 'YYYY-MM-DD'
        }
        """
        if self.use_mongo:
            return self.db.curriculum.update_one(
                {'degree': entry.get('degree'), 'year': entry.get('year')},
                {'$set': entry},
                upsert=True
            )

        data = self._read()
        items = data.get('curriculum', [])

        # replace if exists
        replaced = False
        for i, it in enumerate(items):
            if it.get('degree') == entry.get('degree') and it.get('year') == entry.get('year'):
                items[i] = entry
                replaced = True
                break

        if not replaced:
            items.append(entry)

        data['curriculum'] = items
        self._write(data)
        return True

    def delete_curriculum(self, degree, year):
        if self.use_mongo:
            return self.db.curriculum.delete_one(
                {'degree': degree, 'year': year}
            )

        data = self._read()
        items = data.get('curriculum', [])
        items = [
            it for it in items
            if not (it.get('degree') == degree and it.get('year') == year)
        ]
        data['curriculum'] = items
        self._write(data)
        return True

    # ---------- ALUMNI / TESTIMONIALS ----------
    def list_alumni(self):
        if self.use_mongo:
            records = list(self.db.alumni.find())
            for r in records:
                r.pop("_id", None)
            return records

        data = self._read()
        return data.get("alumni", [])

    def add_alumni(self, entry):
        if self.use_mongo:
            return self.db.alumni.insert_one(entry).inserted_id

        data = self._read()
        data.setdefault("alumni", []).append(entry)
        self._write(data)
        return True

    def delete_alumni(self, aid):
        if self.use_mongo:
            return self.db.alumni.delete_one({"id": aid})

        data = self._read()
        data["alumni"] = [a for a in data.get("alumni", []) if a.get("id") != aid]
        self._write(data)
        return True

