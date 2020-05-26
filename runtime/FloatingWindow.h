////////////////////////////////////////////////////////////////////////////
//
// Hospital HMIS - DHIS2 Tools
//
// Copyright (C) 2020, GRZ Ministry of Health
// This software is released under the GNU General Public License v3.0
//
// FloatingWindow.h - For GNOME 3.26 and above floating window will be used.
//
////////////////////////////////////////////////////////////////////////////


#ifndef FLOATINGWINDOW_H
#define FLOATINGWINDOW_H

#include "pgAdmin4.h"
#include "MenuActions.h"

#include <QMainWindow>

namespace Ui {
class FloatingWindow;
}

class FloatingWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit FloatingWindow(QWidget *parent = Q_NULLPTR);
    ~FloatingWindow();

    bool Init();
    void enableShutdownMenu();
    void setMenuActions(MenuActions * menuActions);

private:
    Ui::FloatingWindow *ui;

    void createMenu();
    void createActions();
    void closeEvent(QCloseEvent * event);

    QAction *m_newAction;
    QAction *m_copyUrlAction;
    QAction *m_configAction;
    QAction *m_logAction;
    QAction *m_quitAction;

    QMenu *m_floatingWindowMenu;
    MenuActions *m_menuActions;

signals:
    void shutdownSignal(QUrl);
};

#endif // FLOATINGWINDOW_H
