# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARKspatial
                    A QGIS plugin for Archaeological Recording.
        Part of the Archaeological Recording Kit by L - P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        copyright            : 2017 by L - P : Heritage LLP
        email                : ark@lparchaeology.com
        copyright            : 2017 by John Layt
        email                : john@layt.net
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import webbrowser

from PyQt4.QtGui import QAction, QApplication


class OpenArkAction(QAction):

    def __init__(self, arkUrl, item, label, parent=None):
        super(OpenArkAction, self).__init__(label, parent)
        mod_cd = item.classCode() + '_cd'
        item = item.siteCode() + '_' + item.itemId()
        self._url = arkUrl + '/micro_view.php?item_key=' + mod_cd + '&' + mod_cd + '=' + item
        self.triggered.connect(self._open)

    def _open(self):
        QApplication.clipboard().setText(self._url)
        try:
            webbrowser.get().open_new_tab(self._url)
        except Exception:
            self._plugin.showWarningMessage('Unable to open browser, ARK link has been copied to the clipboard')
