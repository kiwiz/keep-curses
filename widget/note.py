# -*- coding: utf-8 -*-
import urwid
import constants
import gkeepapi
import logging

from typing import List

class Labels(urwid.Columns):
    def __init__(self):
        super(Labels, self).__init__([], dividechars=1)

    def setLabels(self, labels: List[gkeepapi.node.Label], color: gkeepapi.node.ColorValue):
        self.contents = [
            (urwid.Text(('l' + color.value, label.name)), self.options(urwid.PACK)) for label in labels
        ]

class Note(urwid.AttrMap):
    def __init__(self, note: gkeepapi.node.TopLevelNode):
        self.note = note

        tmp = urwid.Text('')

        self.w_title = urwid.Text(u'', wrap=urwid.CLIP)
        self.w_text = urwid.Text(u'')
        self.w_labels = Labels()

        self.w_header = urwid.Text(u'', align=urwid.RIGHT)
        self.w_footer = urwid.Text(u'', align=urwid.RIGHT)
        self.w_content = urwid.Frame(
            urwid.Filler(self.w_text, valign=urwid.TOP),
            header=tmp,
            footer=tmp
        )

        super(Note, self).__init__(
            urwid.Frame(
                urwid.Padding(
                    self.w_content,
                    align='center',
                    left=1,
                    right=1
                ),
                header=self.w_header,
                footer=self.w_footer,
            ),
            note.color.value,
            'GREEN'
        )

        self._updateContent()
        self._updateLabels()
        self._updatePinned()
        self._updateArchived()

    def _updateContent(self):
        w_title = (None, self.w_content.options())
        if self.note.title:
            w_title = (self.w_title, self.w_content.options())
            self.w_title.set_text(('b' + self.note.color.value, self.note.title))

        self.w_content.contents['header'] = w_title
        self.w_text.set_text(self.note.text)

    def _updateLabels(self):
        w_labels = (None, self.w_content.options())
        if len(self.note.labels):
            w_labels = (self.w_labels, self.w_content.options())
            self.w_labels.setLabels(self.note.labels.all(), self.note.color)

        self.w_content.contents['footer'] = w_labels

    def _updateArchived(self):
        self.w_footer.set_text('📥' if self.note.archived else '')

    def _updatePinned(self):
        self.w_header.set_text('📍' if self.note.pinned else '')

    def keypress(self, size, key):
        if key == 'f':
            self.note.pinned = not self.note.pinned
            self._updatePinned()
            key = None
        elif key == 'e':
            self.note.archived = not self.note.archived
            self._updateArchived()
            key = None

        super(Note, self).keypress(size, key)
        return key
