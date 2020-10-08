from typing import List, Optional


class Author:

    def __init__(self, data: dict):
        self.type = data.get('creatorType', 'author')
        self.firstname = data.get('firstName', '')
        self.lastname = data.get('lastName', None)

    def serialize(self):
        return {
            'type': self.type,
            'firstname': self.firstname,
            'lastname': self.lastname,
        }


class Attachment:

    def __init__(self, data: dict):
        self.bytesize = data.get('attachmentSize', 0)  # type: int
        self.type = data.get('attachmentType', None)  # type: Optional[str]
        self.href = data.get('href', None)  # type: Optional[str]
        self.key = None
        if self.href is not None:
            self.key = self.href.split('/')[-1]

    @staticmethod
    def from_links(links: dict):
        if 'attachment' in links.keys():
            return [Attachment(links['attachment'])]
        return []

    def serialize(self):
        return {
            'bytesize': self.bytesize,
            'type': self.type,
            'href': self.href,
            'key': self.key,
        }


class AttachmentMetadata:

    def __init__(self, item: dict):
        data = item['data']
        self.key = data.get('key', 'unknown')  # type: str
        self.parent = data.get('parent', None)  # type: Optional[str]
        self.file_hash = data.get('md5', None)  # type: Optional[str]
        self.mtime = data.get('mtime', None)  # type: Optional[str]
        self.title = data.get('title', '')  # type: str
        self.filename = data.get('filename', self.key)  # type: str
        self.content_type = data.get('contentType', 'application/octet-stream')  # type: str
        self.tags = [tag['tag'] for tag in data.get('tags', [])]  # type: List[str]

    def serialize(self):
        return {
            'key': self.key,
            'parent': self.parent,
            'file_hash': self.file_hash,
            'mtime': self.mtime,
            'title': self.title,
            'filename': self.filename,
            'content_type': self.content_type,
            'tags': self.tags,
        }


class LibraryItem:

    def __init__(self, item: dict):
        data = item['data']
        self.key = data.get('key', 'unknown')  # type: str
        self.title = data.get('title', '(no title given)')  # type: str
        self.type = data.get('itemType', 'unknown')  # type: str
        self.date = data.get('date', None)  # type: Optional[str]
        self.doi = data.get('DOI', None)  # type: Optional[str]
        self.isbn = data.get('ISBN', None)  # type: Optional[str]
        self.issn = data.get('ISSN', None)  # type: Optional[str]
        self.publisher = data.get('publisher', None)  # type: Optional[str]
        self.pages = data.get('pages', None)  # type: Optional[str]
        self.conference_name = data.get('conferenceName', None)  # type: Optional[str]
        self.proceedings_title = data.get('proceedingsTitle', None)  # type: Optional[str]
        self.publication_title = data.get('publicationTitle', None)  # type: Optional[str]
        self.journal_abbreviation = data.get('journalAbbreviation', None)  # type: Optional[str]
        self.url = data.get('url', None)  # type: Optional[str]
        self.volume = data.get('volume', None)  # type: Optional[str]
        self.series = data.get('series', None)  # type: Optional[str]
        self.issue = data.get('issue', None)  # type: Optional[str]

        self.authors = [Author(x) for x in data.get('creators', [])]  # type: List[Author]
        self.attachments = Attachment.from_links(item.get('links', []))  # type: List[Attachment]
        self.tags = [tag['tag'] for tag in data.get('tags', [])]  # type: List[str]

    def serialize(self):
        return {
            'key': self.key,
            'title': self.title,
            'type': self.type,
            'date': self.date,
            'doi': self.doi,
            'isbn': self.isbn,
            'issn': self.issn,
            'publisher': self.publisher,
            'pages': self.pages,
            'conferenceName': self.conference_name,
            'proceedingsTitle': self.proceedings_title,
            'publicationTitle': self.publication_title,
            'journalAbbreviation': self.journal_abbreviation,
            'url': self.url,
            'volume': self.volume,
            'series': self.series,
            'issue': self.issue,
            'authors': [a.serialize() for a in self.authors],
            'attachments': [a.serialize() for a in self.attachments],
            'tags': self.tags,
        }
