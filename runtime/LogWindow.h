//////////////////////////////////////////////////////////////////////////
//
// Hospital HMIS - DHIS2 Tools
//
// Copyright (C) 2020, GRZ Ministry of Health
// This software is released under the GNU General Public License v3.0
//
// LogWindow.h - Log viewer window
//
//////////////////////////////////////////////////////////////////////////

#ifndef LOGWINDOW_H
#define LOGWINDOW_H

#include <QDialog>
#include <QPlainTextEdit>

namespace Ui {
class LogWindow;
}

class LogWindow : public QDialog
{
    Q_OBJECT

public:
    explicit LogWindow(QWidget *parent = Q_NULLPTR, QString serverLogFile = "");
    ~LogWindow();

    void LoadLog();

private slots:
    void reload();

private:
    Ui::LogWindow *ui;

    QString m_startupLogFile;
    QString m_serverLogFile;

    int readLog(QString logFile, QPlainTextEdit *logWidget);
};

#endif // LOGWINDOW_H
