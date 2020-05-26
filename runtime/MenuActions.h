//////////////////////////////////////////////////////////////////////////
//
// Hospital HMIS - DHIS2 Tools
//
// Copyright (C) 2020, GRZ Ministry of Health
// This software is released under the GNU General Public License v3.0
//
// MenuActions.h - Common file for menu actions.
//
//////////////////////////////////////////////////////////////////////////

#ifndef MENUACTIONS_H
#define MENUACTIONS_H

#include "pgAdmin4.h"

// App headers
#include "LogWindow.h"
#include "ConfigWindow.h"

class MenuActions: public QObject
{
    Q_OBJECT
public:
    MenuActions();
    ~MenuActions();

    void setAppServerUrl(QString appServerUrl);
    void setLogFile(QString logFile);
    QString getAppServerUrl() { return m_appServerUrl; }

private:
    QString m_appServerUrl, m_logFile;
    LogWindow *m_logWindow;

protected slots:
    void onNew();
    void onCopyUrl();
    void onConfig();
    void onLog();
    void onQuit();

signals:
    void shutdownSignal(QUrl);
};

#endif // MENUACTIONS_H
