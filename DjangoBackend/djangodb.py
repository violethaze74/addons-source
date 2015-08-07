# Gramps - a GTK+/GNOME based genealogy program
#
# Copyright (C) 2009         Douglas S. Blank <doug.blank@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

""" Implements a Db interface """

#------------------------------------------------------------------------
#
# Gramps Modules
#
#------------------------------------------------------------------------
from gramps.gen.db.generic import *
from gramps.gen.const import GRAMPS_LOCALE as glocale
_ = glocale.translation.gettext

## add this directory to sys path, so we can find django_support later:
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class DbDjango(DbGeneric):

    def restore(self):
        pass

    def prepare_import(self):
        """
        DbDjango does not commit data on gedcom import, but saves them
        for later commit.
        """
        self.use_import_cache = True
        self.import_cache = {}

    def commit_import(self):
        """
        Commits the items that were queued up during the last gedcom
        import for two step adding.
        """
        # First we add the primary objects:
        for key in list(self.import_cache.keys()):
            obj = self.import_cache[key]
            if isinstance(obj, Person):
                self.dji.add_person(obj.serialize())
            elif isinstance(obj, Family):
                self.dji.add_family(obj.serialize())
            elif isinstance(obj, Event):
                self.dji.add_event(obj.serialize())
            elif isinstance(obj, Place):
                self.dji.add_place(obj.serialize())
            elif isinstance(obj, Repository):
                self.dji.add_repository(obj.serialize())
            elif isinstance(obj, Citation):
                self.dji.add_citation(obj.serialize())
            elif isinstance(obj, Source):
                self.dji.add_source(obj.serialize())
            elif isinstance(obj, Note):
                self.dji.add_note(obj.serialize())
            elif isinstance(obj, MediaObject):
                self.dji.add_media(obj.serialize())
            elif isinstance(obj, Tag):
                self.dji.add_tag(obj.serialize())
        # Next we add the links:
        for key in list(self.import_cache.keys()):
            obj = self.import_cache[key]
            if isinstance(obj, Person):
                self.dji.add_person_detail(obj.serialize())
            elif isinstance(obj, Family):
                self.dji.add_family_detail(obj.serialize())
            elif isinstance(obj, Event):
                self.dji.add_event_detail(obj.serialize())
            elif isinstance(obj, Place):
                self.dji.add_place_detail(obj.serialize())
            elif isinstance(obj, Repository):
                self.dji.add_repository_detail(obj.serialize())
            elif isinstance(obj, Citation):
                self.dji.add_citation_detail(obj.serialize())
            elif isinstance(obj, Source):
                self.dji.add_source_detail(obj.serialize())
            elif isinstance(obj, Note):
                self.dji.add_note_detail(obj.serialize())
            elif isinstance(obj, MediaObject):
                self.dji.add_media_detail(obj.serialize())
            elif isinstance(obj, Tag):
                self.dji.add_tag_detail(obj.serialize())
        self.use_import_cache = False
        self.import_cache = {}
        self.request_rebuild()

    def write_version(self, directory):
        """Write files for a newly created DB."""
        versionpath = os.path.join(directory, str(DBBACKEND))
        LOG.debug("Write database backend file to 'djangodb'")
        with open(versionpath, "w") as version_file:
            version_file.write("djangodb")
        # Write default_settings, sqlite.db
        defaults = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "django_support", "defaults")
        LOG.debug("Copy defaults from: " + defaults)
        for filename in os.listdir(defaults):
            fullpath = os.path.abspath(os.path.join(defaults, filename))
            shutil.copy2(fullpath, directory)
        # force load, to get all modules loaded because of reset issue
        self.load(directory)

    def initialize_backend(self, directory):
        self.use_import_cache = False
        self._metadata = {}

    def close_backend(self):
        pass
        
    def transaction_commit(self, txn):
        pass

    def transaction_abort(self, txn):
        pass

    def get_metadata(self, key, default=[]):
        if key in self._metadata:
            return self._metadata[key]
        elif default == []:
            return []
        else:
            return default

    def set_metadata(self, key, value):
        self._metadata[key] = value

    def get_name_group_keys(self):
        return []

    def get_name_group_mapping(self, key):
        return None

    def get_person_handles(self, sort_handles=False):
        if sort_handles:
            return [item.handle for item in self.dji.Person.all().order_by("handle")]
        else:
            return [item.handle for item in self.dji.Person.all()]

    def get_family_handles(self):
        return [item.handle for item in self.dji.Family.all()]

    def get_event_handles(self):
        return [item.handle for item in self.dji.Event.all()]

    def get_citation_handles(self, sort_handles=False):
        if sort_handles:
            return [item.handle for item in self.dji.Citation.all().order_by("handle")]
        else:
            return [item.handle for item in self.dji.Citation.all()]

    def get_source_handles(self, sort_handles=False):
        if sort_handles:
            return [item.handle for item in self.dji.Source.all().order_by("handle")]
        else:
            return [item.handle for item in self.dji.Source.all()]

    def get_place_handles(self, sort_handles=False):
        if sort_handles:
            return [item.handle for item in self.dji.Place.all().order_by("handle")]
        else:
            return [item.handle for item in self.dji.Place.all()]

    def get_repository_handles(self):
        return [item.handle for item in self.dji.Repository.all()]

    def get_media_object_handles(self, sort_handles=False):
        if sort_handles:
            return [item.handle for item in self.dji.Media.all().order_by("handle")]
        else:
            return [item.handle for item in self.dji.Media.all()]

    def get_note_handles(self):
        return [item.handle for item in self.dji.Note.all()]

    def get_tag_handles(self, sort_handles=False):
        if sort_handles:
            return [item.handle for item in self.dji.Tag.all().order_by("handle")]
        else:
            return [item.handle for item in self.dji.Tag.all()]

    def get_tag_from_name(self, name):
        try:
            tag = self.dji.Tag.filter(name=name)
            return self._make_tag(tag[0])
        except:
            return None

    def get_number_of_people(self):
        return self.dji.Person.count()

    def get_number_of_events(self):
        return self.dji.Event.count()

    def get_number_of_places(self):
        return self.dji.Place.count()

    def get_number_of_tags(self):
        return self.dji.Tag.count()

    def get_number_of_families(self):
        return self.dji.Family.count()

    def get_number_of_notes(self):
        return self.dji.Note.count()

    def get_number_of_citations(self):
        return self.dji.Citation.count()

    def get_number_of_sources(self):
        return self.dji.Source.count()

    def get_number_of_media_objects(self):
        return self.dji.Media.count()

    def get_number_of_repositories(self):
        return self.dji.Repository.count()

    def has_name_group_key(self, key):
        # FIXME:
        return False

    def set_name_group_mapping(self, name, grouping):
        # FIXME:
        pass

    def commit_person(self, person, trans, change_time=None):
        if self.use_import_cache:
            self.import_cache[person.handle] = person
        else:
            raw = person.serialize()
            items = self.dji.Person.filter(handle=person.handle)
            count = items.count()
            if count > 0:
                # Hack, for the moment: delete and re-add
                items[0].delete()
            self.dji.add_person(person.serialize())
            self.dji.add_person_detail(person.serialize())
            if not trans.batch:
                if count > 0:
                    self.emit("person-update", ([person.handle],))
                else:
                    self.emit("person-add", ([person.handle],))

    def commit_family(self, family, trans, change_time=None):
        if self.use_import_cache:
            self.import_cache[family.handle] = family
        else:
            raw = family.serialize()
            items = self.dji.Family.filter(handle=family.handle)
            count = items.count()
            if count > 0:
                items[0].delete()
            self.dji.add_family(family.serialize())
            self.dji.add_family_detail(family.serialize())
            if not trans.batch:
                if count > 0:
                    self.emit("family-update", ([family.handle],))
                else:
                    self.emit("family-add", ([family.handle],))

    def commit_citation(self, citation, trans, change_time=None):
        if self.use_import_cache:
            self.import_cache[citation.handle] = citation
        else:
            raw = citation.serialize()
            items = self.dji.Citation.filter(handle=citation.handle)
            count = items.count()
            if count > 0:
                items[0].delete()
            self.dji.add_citation(citation.serialize())
            self.dji.add_citation_detail(citation.serialize())
            if not trans.batch:
                if count > 0:
                    self.emit("citation-update", ([citation.handle],))
                else:
                    self.emit("citation-add", ([citation.handle],))

    def commit_source(self, source, trans, change_time=None):
        if self.use_import_cache:
            self.import_cache[source.handle] = source
        else:
            raw = source.serialize()
            items = self.dji.Source.filter(handle=source.handle)
            count = items.count()
            if count > 0:
                items[0].delete()
            self.dji.add_source(source.serialize())
            self.dji.add_source_detail(source.serialize())
            if not trans.batch:
                if count > 0:
                    self.emit("source-update", ([source.handle],))
                else:
                    self.emit("source-add", ([source.handle],))

    def commit_repository(self, repository, trans, change_time=None):
        if self.use_import_cache:
            self.import_cache[repository.handle] = repository
        else:
            raw = repository.serialize()
            items = self.dji.Repository.filter(handle=repository.handle)
            count = items.count()
            if count > 0:
                items[0].delete()
            self.dji.add_repository(repository.serialize())
            self.dji.add_repository_detail(repository.serialize())
            if not trans.batch:
                if count > 0:
                    self.emit("repository-update", ([repository.handle],))
                else:
                    self.emit("repository-add", ([repository.handle],))

    def commit_note(self, note, trans, change_time=None):
        if self.use_import_cache:
            self.import_cache[note.handle] = note
        else:
            raw = note.serialize()
            items = self.dji.Note.filter(handle=note.handle)
            count = items.count()
            if count > 0:
                items[0].delete()
            self.dji.add_note(note.serialize())
            self.dji.add_note_detail(note.serialize())
            if not trans.batch:
                if count > 0:
                    self.emit("note-update", ([note.handle],))
                else:
                    self.emit("note-add", ([note.handle],))

    def commit_place(self, place, trans, change_time=None):
        if self.use_import_cache:
            self.import_cache[place.handle] = place
        else:
            raw = place.serialize()
            items = self.dji.Place.filter(handle=place.handle)
            count = items.count()
            if count > 0:
                items[0].delete()
            self.dji.add_place(place.serialize())
            self.dji.add_place_detail(place.serialize())
            if not trans.batch:
                if count > 0:
                    self.emit("place-update", ([place.handle],))
                else:
                    self.emit("place-add", ([place.handle],))

    def commit_event(self, event, trans, change_time=None):
        if self.use_import_cache:
            self.import_cache[event.handle] = event
        else:
            raw = event.serialize()
            items = self.dji.Event.filter(handle=event.handle)
            count = items.count()
            if count > 0:
                items[0].delete()
            self.dji.add_event(event.serialize())
            self.dji.add_event_detail(event.serialize())
            if not trans.batch:
                if count > 0:
                    self.emit("event-update", ([event.handle],))
                else:
                    self.emit("event-add", ([event.handle],))

    def commit_tag(self, tag, trans, change_time=None):
        if self.use_import_cache:
            self.import_cache[tag.handle] = tag
        else:
            raw = tag.serialize()
            items = self.dji.Tag.filter(handle=tag.handle)
            count = items.count()
            if count > 0:
                items[0].delete()
            self.dji.add_tag(tag.serialize())
            self.dji.add_tag_detail(tag.serialize())
            if not trans.batch:
                if count > 0:
                    self.emit("tag-update", ([tag.handle],))
                else:
                    self.emit("tag-add", ([tag.handle],))

    def commit_media_object(self, media, trans, change_time=None):
        """
        Commit the specified MediaObject to the database, storing the changes
        as part of the transaction.
        """
        if self.use_import_cache:
            self.import_cache[media.handle] = media
        else:
            raw = media.serialize()
            items = self.dji.Media.filter(handle=media.handle)
            count = items.count()
            if count > 0:
                items[0].delete()
            self.dji.add_media(media.serialize())
            self.dji.add_media_detail(media.serialize())
            if not trans.batch:
                if count > 0:
                    self.emit("media-update", ([media.handle],))
                else:
                    self.emit("media-add", ([media.handle],))

    def update_backlinks(self, obj):
        pass

    # Removals:
    def remove_person(self, handle, transaction):
        self.dji.Person.filter(handle=handle)[0].delete()
        self.emit("person-delete", ([handle],))

    def _do_remove(self, handle, transaction, data_map, data_id_map, key):
        key2table = {
            PERSON_KEY:     "person", 
            FAMILY_KEY:     "family", 
            SOURCE_KEY:     "source", 
            CITATION_KEY:   "citation", 
            EVENT_KEY:      "event", 
            MEDIA_KEY:      "media", 
            PLACE_KEY:      "place", 
            REPOSITORY_KEY: "repository", 
            NOTE_KEY:       "note", 
            }
        table = getattr(self.dji, key2table[key].title())
        table.filter(handle=handle)[0].delete()
        self.emit("%s-delete" % key2table[key], ([handle],))

    def find_backlink_handles(self, handle, include_classes=None):
        return []

    def find_initial_person(self):
        handle = self.get_default_handle()
        person = None
        if handle:
            person = self.get_person_from_handle(handle)
            if person:
                return person
        if len(self.dji.Person.all()) > 0:
            person = self.dji.Person.all()[0]
            return self.get_person_from_handle(person.handle)

    def iter_person_handles(self):
        return (person.handle for person in self.dji.Person.all())

    def iter_family_handles(self):
        return (family.handle for family in self.dji.Family.all())

    def iter_citation_handles(self):
        return (citation.handle for citation in self.dji.Citation.all())

    def iter_event_handles(self):
        return (event.handle for event in self.dji.Event.all())

    def iter_media_object_handles(self):
        return (media.handle for media in self.dji.Media.all())

    def iter_note_handles(self):
        return (note.handle for note in self.dji.Note.all())

    def iter_place_handles(self):
        return (place.handle for place in self.dji.Place.all())

    def iter_repository_handles(self):
        return (repository.handle for repository in self.dji.Repository.all())

    def iter_source_handles(self):
        return (source.handle for source in self.dji.Source.all())

    def iter_tag_handles(self):
        return (tag.handle for tag in self.dji.Tag.all())

    def reindex_reference_map(self, callback):
        pass

    def rebuild_secondary(self, update):
        pass

    def has_handle_for_person(self, key):
        return self.dji.Person.filter(handle=key).count() > 0

    def has_handle_for_family(self, key):
        return self.dji.Person.filter(handle=key).count() > 0

    def has_handle_for_source(self, key):
        return self.dji.Person.filter(handle=key).count() > 0

    def has_handle_for_citation(self, key):
        return self.dji.Person.filter(handle=key).count() > 0

    def has_handle_for_event(self, key):
        return self.dji.Event.filter(handle=key).count() > 0

    def has_handle_for_media(self, key):
        return self.dji.Media.filter(handle=key).count() > 0

    def has_handle_for_place(self, key):
        return self.dji.Place.filter(handle=key).count() > 0

    def has_handle_for_repository(self, key):
        return self.dji.Repository.filter(handle=key).count() > 0

    def has_handle_for_note(self, key):
        return self.dji.Note.filter(handle=key).count() > 0

    def has_handle_for_tag(self, key):
        return self.dji.Tag.filter(handle=key).count() > 0

    def has_gramps_id_for_person(self, key):
        return self.dji.Person.filter(gramps_id=key).count() > 0

    def has_gramps_id_for_family(self, key):
        return self.dji.Family.filter(gramps_id=key).count() > 0

    def has_gramps_id_for_source(self, key):
        return self.dji.Source.filter(gramps_id=key).count() > 0

    def has_gramps_id_for_citation(self, key):
        return self.dji.Citation.filter(gramps_id=key).count() > 0

    def has_gramps_id_for_event(self, key):
        return self.dji.Event.filter(gramps_id=key).count() > 0

    def has_gramps_id_for_media(self, key):
        return self.dji.Media.filter(gramps_id=key).count() > 0

    def has_gramps_id_for_place(self, key):
        return self.dji.Place.filter(gramps_id=key).count() > 0

    def has_gramps_id_for_repository(self, key):
        return self.dji.Repository.filter(gramps_id=key).count() > 0

    def has_gramps_id_for_note(self, key):
        return self.dji.Note.filter(gramps_id=key).count() > 0

    def get_person_gramps_ids(self):
        return [x.gramps_id for x in self.dji.Person.all()]

    def get_family_gramps_ids(self):
        return [x.gramps_id for x in self.dji.Family.all()]

    def get_source_gramps_ids(self):
        return [x.gramps_id for x in self.dji.Source.all()]

    def get_citation_gramps_ids(self):
        return [x.gramps_id for x in self.dji.Citation.all()]

    def get_event_gramps_ids(self):
        return [x.gramps_id for x in self.dji.Event.all()]

    def get_media_gramps_ids(self):
        return [x.gramps_id for x in self.dji.Media.all()]

    def get_place_gramps_ids(self):
        return [x.gramps_id for x in self.dji.Place.all()]

    def get_repository_gramps_ids(self):
        return [x.gramps_id for x in self.dji.Repository.all()]

    def get_note_gramps_ids(self):
        return [x.gramps_id for x in self.dji.Note.all()]

    def _get_raw_person_data(self, key):
        try:
            return self.dji.get_person(self.dji.Person.get(handle=key))
        except:
            if key in self.import_cache:
                return self.import_cache[key].serialize()
            else:
                return None

    def _get_raw_person_from_id_data(self, key):
        try:
            return self.dji.get_person(self.dji.Person.get(gramps_id=key))
        except:
            for item in self.import_cache.values():
                if item.gramps_id == key:
                    return item.serialize()

    def _get_raw_family_data(self, key):
        try:
            return self.dji.get_family(self.dji.Family.get(handle=key))
        except:
            if key in self.import_cache:
                return self.import_cache[key].serialize()
            else:
                return None

    def _get_raw_family_from_id_data(self, key):
        try:
            return self.dji.get_person(self.dji.Family.get(gramps_id=key))
        except:
            for item in self.import_cache.values():
                if item.gramps_id == key:
                    return item.serialize()

    def _get_raw_source_data(self, key):
        try:
            return self.dji.get_source(self.dji.Source.get(handle=key))
        except:
            if key in self.import_cache:
                return self.import_cache[key].serialize()
            else:
                return None

    def _get_raw_source_from_id_data(self, key):
        try:
            return self.dji.get_person(self.dji.Source.get(gramps_id=key))
        except:
            for item in self.import_cache.values():
                if item.gramps_id == key:
                    return item.serialize()

    def _get_raw_citation_data(self, key):
        try:
            return self.dji.get_citation(self.dji.Citation.get(handle=key))
        except:
            if key in self.import_cache:
                return self.import_cache[key].serialize()
            else:
                return None

    def _get_raw_citation_from_id_data(self, key):
        try:
            return self.dji.get_person(self.dji.Citation.get(gramps_id=key))
        except:
            for item in self.import_cache.values():
                if item.gramps_id == key:
                    return item.serialize()

    def _get_raw_event_data(self, key):
        try:
            return self.dji.get_event(self.dji.Event.get(handle=key))
        except:
            if key in self.import_cache:
                return self.import_cache[key].serialize()
            else:
                return None

    def _get_raw_event_from_id_data(self, key):
        try:
            return self.dji.get_person(self.dji.Event.get(gramps_id=key))
        except:
            for item in self.import_cache.values():
                if item.gramps_id == key:
                    return item.serialize()

    def _get_raw_media_data(self, key):
        try:
            return self.dji.get_media(self.dji.Media.get(handle=key))
        except:
            if key in self.import_cache:
                return self.import_cache[key].serialize()
            else:
                return None

    def _get_raw_media_from_id_data(self, key):
        try:
            return self.dji.get_person(self.dji.Media.get(gramps_id=key))
        except:
            for item in self.import_cache.values():
                if item.gramps_id == key:
                    return item.serialize()

    def _get_raw_place_data(self, key):
        try:
            return self.dji.get_place(self.dji.Place.get(handle=key))
        except:
            if key in self.import_cache:
                return self.import_cache[key].serialize()
            else:
                return None

    def _get_raw_place_from_id_data(self, key):
        try:
            return self.dji.get_person(self.dji.Place.get(gramps_id=key))
        except:
            for item in self.import_cache.values():
                if item.gramps_id == key:
                    return item.serialize()

    def _get_raw_repository_data(self, key):
        try:
            return self.dji.get_repository(self.dji.Repository.get(handle=key))
        except:
            if key in self.import_cache:
                return self.import_cache[key].serialize()
            else:
                return None

    def _get_raw_repository_from_id_data(self, key):
        try:
            return self.dji.get_person(self.dji.Repository.get(gramps_id=key))
        except:
            for item in self.import_cache.values():
                if item.gramps_id == key:
                    return item.serialize()

    def _get_raw_note_data(self, key):
        try:
            return self.dji.get_note(self.dji.Note.get(handle=key))
        except:
            if key in self.import_cache:
                return self.import_cache[key].serialize()
            else:
                return None

    def _get_raw_note_from_id_data(self, key):
        try:
            return self.dji.get_person(self.dji.Note.get(gramps_id=key))
        except:
            for item in self.import_cache.values():
                if item.gramps_id == key:
                    return item.serialize()

    def _get_raw_tag_data(self, key):
        try:
            return self.dji.get_tag(self.dji.Tag.get(handle=key))
        except:
            if key in self.import_cache:
                return self.import_cache[key].serialize()
            else:
                return None

    def rebuild_gender_stats(self):
        """
        Returns a dictionary of 
        {given_name: (male_count, female_count, unknown_count)} 
        """
        return {}

    def save_gender_stats(self, gstats):
        # FIXME: save
        pass

    def get_gender_stats(self):
        """
        Returns a dictionary of 
        {given_name: (male_count, female_count, unknown_count)} 
        """
        # FIXME: load?
        return {}

    def get_surname_list(self):
        return []

    def save_surname_list(self):
        pass

    def build_surname_list(self):
        pass

    def drop_tables(self):
        pass

    def load(self, directory, callback=None, mode=None, 
             force_schema_upgrade=False, 
             force_bsddb_upgrade=False, 
             force_bsddb_downgrade=False, 
             force_python_upgrade=False):
        super().load(directory, 
                     callback, 
                     mode, 
                     force_schema_upgrade, 
                     force_bsddb_upgrade, 
                     force_bsddb_downgrade, 
                     force_python_upgrade)
        # Django-specific loads:
        from django.conf import settings

        LOG.info("Django loading...")
        default_settings = {"__file__": 
                            os.path.join(self._directory, "default_settings.py")}
        settings_file = os.path.join(self._directory, "default_settings.py")
        with open(settings_file) as f:
            code = compile(f.read(), settings_file, 'exec')
            exec(code, globals(), default_settings)

        class Module(object):
            def __init__(self, dictionary):
                self.dictionary = dictionary
            def __getattr__(self, item):
                return self.dictionary[item]

        LOG.info("Django loading defaults from: " + self._directory)
        try:
            settings.configure(Module(default_settings))
        except RuntimeError:
            LOG.info("Django already configured error! Shouldn't happen!")
            # already configured; ignore

        import django
        django.setup()

        from django_support.libdjango import DjangoInterface

        self.dji = DjangoInterface()

    def _make_repository(self, repository):
        if self.use_db_cache and repository.cache:
            data = repository.from_cache()
        else:
            data = self.dji.get_repository(repository)
        return Repository.create(data)

    def _make_citation(self, citation):
        if self.use_db_cache and citation.cache:
            data = citation.from_cache()
        else:
            data = self.dji.get_citation(citation)
        return Citation.create(data)

    def _make_source(self, source):
        if self.use_db_cache and source.cache:
            data = source.from_cache()
        else:
            data = self.dji.get_source(source)
        return Source.create(data)

    def _make_family(self, family):
        if self.use_db_cache and family.cache:
            data = family.from_cache()
        else:
            data = self.dji.get_family(family)
        return Family.create(data)

    def _make_person(self, person):
        if self.use_db_cache and person.cache:
            data = person.from_cache()
        else:
            data = self.dji.get_person(person)
        return Person.create(data)

    def _make_event(self, event):
        if self.use_db_cache and event.cache:
            data = event.from_cache()
        else:
            data = self.dji.get_event(event)
        return Event.create(data)

    def _make_note(self, note):
        if self.use_db_cache and note.cache:
            data = note.from_cache()
        else:
            data = self.dji.get_note(note)
        return Note.create(data)

    def _make_tag(self, tag):
        data = self.dji.get_tag(tag)
        return Tag.create(data)

    def _make_place(self, place):
        if self.use_db_cache and place.cache:
            data = place.from_cache()
        else:
            data = self.dji.get_place(place)
        return Place.create(data)

    def _make_media(self, media): 
        if self.use_db_cache and media.cache:
            data = media.from_cache()
        else:
            data = self.dji.get_media(media)
        return MediaObject.create(data)

    def request_rebuild(self): # override
        # caches are ok, but let's compute public's
        self.dji.update_publics()
        super().request_rebuild()

